from urllib import response
from django.shortcuts import render, redirect, get_object_or_404
# from matplotlib.style import context
from sqlalchemy import null
from . import forms
from django.contrib import messages
from .models import Plandatas, Rtdatas, Plandatas, Stracturedatas, Ctdatas, Memo
from accounts.models import Users
from django.core.cache import cache
from django.http import JsonResponse
from django.http import Http404
from django.core.files.storage import FileSystemStorage
import os
from datetime import datetime
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import (CreateView, UpdateView, DeleteView, FormView,)
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

import logging
application_logger = logging.getLogger('application-logger')

from .forms import(CreateRtdataForm ,CreateCtdataForm, CreatePlandataForm, CreateStracturedataForm)

import pydicom
import numpy as np

# from matplotlib.style import context

# from turtle import update
# from django.forms import formset_factory,modelformset_factory
# from fsspec import filesystem
# from matplotlib.style import context
# from psutil import users

# Create your views here.
class RtdataDetailView(LoginRequiredMixin, DetailView):
    model = Rtdatas
    template_name = 'analytics/detail_rtdata.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rtdata_id = self.object.id
        plandata = Plandatas.objects.filter(rtdata_id=rtdata_id)
        if plandata.first() is not None:
            file = Plandatas.objects.get(rtdata_id=rtdata_id) ####
            df = pydicom.read_file(file.plandata)
            if 'FractionGroupSequence' in df :
                beam_number = df.FractionGroupSequence[0].NumberOfBeams
                Jaw_ref = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75,
                        80, 85, 90, 95, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]
                Jaw_ref2 = [0, -5, -10, -15, -20, -25, -30, -35, -40, -45, -50, -55, -60, -65, -70, -
                            75, -80, -85, -90, -95, -100, -110, -120, -130, -140, -150, -160, -170, -180, -190, -200]

                cp_list = []
                for i in range(beam_number):
                    cp = df.BeamSequence[i].NumberOfControlPoints
                    cp_list.append(cp)

                cp_sum = sum(cp_list)

                tmp_x  = xjaw_position(df, beam_number)
                xjaw = beamnumber_split(tmp_x, beam_number, cp_list)
                tmp_y = yjaw_position(df, beam_number)
                yjaw = beamnumber_split(tmp_y, beam_number, cp_list)
                tmp_mlc = MLC_position(df, beam_number)
                mlc = beamnumber_split(tmp_mlc, beam_number, cp_list)
                mu = MU_data(df, beam_number)
                tmp_weight = Weight_data(df, beam_number)
                weight = beamnumber_split(tmp_weight, beam_number, cp_list)
                tmp_mu_cp = MU_cp(mu, weight,df, beam_number)
                no_sub_mu_cp = beamnumber_split(tmp_mu_cp, beam_number, cp_list)
                tmp_list = list_sub(no_sub_mu_cp, df, beam_number)
                mu_cp = beamnumber_split(tmp_list, beam_number, cp_list)

                context['plandata'] = df
                context['beamnumber'] = beam_number
                context['xjaw'] = xjaw[0]
                context['yjaw'] = yjaw[0]
                context['mlc'] = mlc[0]
                context['weight'] = weight[0]
                context['mu_cp'] = mu_cp[0]
                context['mu'] = mu

        return context

class RtdataListView(LoginRequiredMixin, ListView):
    model = Rtdatas
    template_name = 'analytics/list_rtdatas.html'

    def get_queryset(self):
        query = super().get_queryset()
        region = self.request.GET.get('region', None)
        author = self.request.GET.get('author', None)
        if region:
            query = query.filter(
                region=region
            )
        if author:
            qs = Users.objects.filter(
                username=author
            )
            query = query.filter(
                user_id=qs[0].id
            )
        order_by_create_at = self.request.GET.get('order_by_create_at', 0)
        if order_by_create_at == '1':
            query = query.order_by('create_at')
        elif order_by_create_at == '2':
            query = query.order_by('-create_at')
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['region'] = self.request.GET.get('region', '')
        context['author'] = self.request.GET.get('author', '')
        order_by_create_at = self.request.GET.get('order_by_create_at', 0)
        if order_by_create_at == '1':
            context['ascending'] = True
        elif order_by_create_at == '2':
            context['descending'] = True
        return context


class RtdataCreateView(LoginRequiredMixin, CreateView):
    model = Rtdatas
    form_class = forms.CreateRtdataForm
    template_name = 'analytics/create_rtdata.html'
    success_url = reverse_lazy('analytics:list_rtdatas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plandata_form = forms.CreatePlandataForm()
        stracturedata_form = forms.CreateStracturedataForm()
        ctdata_form = forms.CreateCtdataForm()
        context['plandata_form'] = plandata_form
        context['stracturedata_form'] = stracturedata_form
        context['ctdata_form'] = ctdata_form

        plandata = Plandatas.objects.filter_by_rtdata(rtdata=self.object)
        stracturedata =  Stracturedatas.objects.filter_by_rtdata(rtdata=self.object)
        ctdata =  Ctdatas.objects.filter_by_rtdata(rtdata=self.object)


        context['plandata'] = plandata
        context['stracturedata'] = stracturedata
        context['ctdata'] = ctdata
        return context


    def post(self, request, *args, **kwargs):
        create_rtdata_form = forms.CreateRtdataForm(request.POST or None)
        if create_rtdata_form.is_valid():
            create_rtdata_form.instance.user = request.user
            create_rtdata_form.instance.create_at = datetime.now()
            create_rtdata_form.instance.update_at = datetime.now()
            create_rtdata_form.save()
            rtdata = Rtdatas.objects.order_by("id").last()

        plandata_form = forms.CreatePlandataForm(request.POST or None, request.FILES or None)
        if plandata_form.is_valid() and 'plandata' in request.FILES: # リクエストファイルを削除して入力させている。
            plandata_form.save(rtdata=rtdata, plandata=request.FILES['plandata'])

        stracturedata_form = forms.CreateStracturedataForm(request.POST or None, request.FILES or None)
        if stracturedata_form.is_valid() and 'stracturedata' in request.FILES :
            stracturedata_form.save(rtdata=rtdata, stracturedata=request.FILES['stracturedata'])

        ctdata_form = forms.CreateCtdataForm(request.POST or None, request.FILES or None)
        if Ctdatas.objects.filter(ctdata='ctdata/' + str(rtdata.pk) + '/'+ str(ctdata_form['ctdata'].data)):
            pass
        elif ctdata_form.is_valid() and 'ctdata' in request.FILES:
            ctdata_form.save(rtdata=rtdata, ctdata=request.FILES['ctdata'])

        return redirect('analytics:list_rtdatas')

    #デフォルト値を設定
    # def get_initial(self, **kwargs):
    #     initial = super(RtdataCreateView, self).get_initial(**kwargs)
    #     initial['region'] = 'sample'
    #     return initial



class RtdataUpdateView(SuccessMessageMixin, UpdateView):
    model = Rtdatas
    template_name = 'analytics/update_rtdata.html'
    form_class = forms.UpdateRtdataForm
    success_message = '更新に成功しました'

    def get_success_url(self):
        return reverse_lazy('analytics:edit_rtdata', kwargs={'pk': self.object.id})

    def get_success_message(self, cleaned_data):
        return cleaned_data.get('region') + 'に更新しました'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plandata_form = forms.PlandataUploadForm()
        plandata = Plandatas.objects.filter_by_rtdata(rtdata=self.object)
        stracturedata_form = forms.StracturedataUploadForm()
        stracturedata =  Stracturedatas.objects.filter_by_rtdata(rtdata=self.object)
        ctdata_form = forms.CtdataUploadForm()
        ctdata =  Ctdatas.objects.filter_by_rtdata(rtdata=self.object)
        rtdata = Rtdatas.objects.get(id=self.object.id)
        context['rtdata'] = rtdata
        context['plandata'] = plandata
        context['plandata_form'] = plandata_form
        context['stracturedata'] = stracturedata
        context['stracturedata_form'] = stracturedata_form
        context['ctdata'] = ctdata
        context['ctdata_form'] = ctdata_form
        return context

    def post(self, request, *args, **kwargs):
        plandata_form = forms.PlandataUploadForm(request.POST or None, request.FILES or None)
        if plandata_form['plandata'].data is None :
            pass
        elif plandata_form.is_valid() and request.FILES:
                rtdata = self.get_object()
                plandata_form.save(rtdata=rtdata)

        stracturedata_form = forms.StracturedataUploadForm(request.POST or None, request.FILES or None)
        if stracturedata_form['stracturedata'].data is None :
            pass
        elif stracturedata_form.is_valid() and request.FILES:
            rtdata = self.get_object()
            stracturedata_form.save(rtdata=rtdata)

        ctdata_form = forms.CtdataUploadForm(request.POST or None, request.FILES or None)
        if ctdata_form['ctdata'].data is None :
            pass
        elif Ctdatas.objects.filter(ctdata='ctdata/' + str(self.kwargs['pk']) + '/'+ str(ctdata_form['ctdata'].data)):
            pass
        elif ctdata_form.is_valid() and request.FILES:
            rtdata = self.get_object()
            ctdata_form.save(rtdata=rtdata)

        return super(RtdataUpdateView, self).post(request, *args, **kwargs)

class RtdataDeleteView(SuccessMessageMixin, DeleteView):
    model = Rtdatas
    template_name = 'analytics/delete_rtdata.html'
    success_url = reverse_lazy('analytics:list_rtdatas')
    success_message = 'データを削除しました'

class RtdataFormView(LoginRequiredMixin, FormView):

    template_name = 'analytics/form_rtdata.html'
    form_class = forms.CreateRtdataForm
    success_url = reverse_lazy('analytics:list_rtdatas')

    def get_initial(self):
        initial = super(RtdataFormView, self).get_initial()
        initial['name'] = 'form sample'
        return initial

    def form_valid(self, form):
        if form.is_valid():
            form.instance.create_at = datetime.now()
            form.instance.update_at = datetime.now()
            form.instance.user = self.request.user
            form.save()
        return super(RtdataFormView, self).form_valid(form)


class ToridogRedirectView(RedirectView):
    url = 'http://52.199.116.176/'

    #     def get_redirect_url(self, *args, **kwargs):
    #         book = Books.objects.first()
    #         if 'pk' in kwargs:
    #             return reverse_lazy('store:detail_book', kwargs={'pk': kwargs['pk']})

    #         return reverse_lazy('store:edit_book', kwargs={'pk': book.pk})

class Jtcs(LoginRequiredMixin, ListView):
    model = Rtdatas
    template_name = 'analytics/jtcs.html'

    def get_queryset(self):
        query = super().get_queryset()
        region = self.request.GET.get('region', None)
        author = self.request.GET.get('author', None)
        if region:
            query = query.filter(
                region=region
            )
        if author:
            qs = Users.objects.filter(
                username=author
            )
            query = query.filter(
                user_id=qs[0].id
            )
        order_by_create_at = self.request.GET.get('order_by_create_at', 0)
        if order_by_create_at == '1':
            query = query.order_by('create_at')
        elif order_by_create_at == '2':
            query = query.order_by('-create_at')
        return query

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['region'] = self.request.GET.get('region', '')
        context['author'] = self.request.GET.get('author', '')
        order_by_create_at = self.request.GET.get('order_by_create_at', 0)
        if order_by_create_at == '1':
            context['ascending'] = True
        elif order_by_create_at == '2':
            context['descending'] = True

        jtcs_data = []
        region = self.request.GET.get('region', None)
        author = self.request.GET.get('author', None)
        if region and author:
            user_id = Users.objects.filter(username=author)
            rtdatas = Rtdatas.objects.filter(region=region, user_id=user_id)
        elif region:
            rtdatas = Rtdatas.objects.filter(region=region)
        elif author:
            user_id = Users.objects.filter(username=author)
            rtdatas = Rtdatas.objects.filter(user_id=user_id)
        else:
            rtdatas = Rtdatas.objects.fetch_all_rtdatas()
        for rtdata in rtdatas:
            rtdata_id = rtdata.id
            plandata = Plandatas.objects.filter(rtdata_id=rtdata_id)
            if plandata.first() is not None:
                        file = Plandatas.objects.get(rtdata_id=rtdata_id)
                        df = pydicom.read_file(file.plandata)
                        if 'FractionGroupSequence' in df :
                            beam_number = df.FractionGroupSequence[0].NumberOfBeams
                            Jaw_ref = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75,
                                    80, 85, 90, 95, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]
                            Jaw_ref2 = [0, -5, -10, -15, -20, -25, -30, -35, -40, -45, -50, -55, -60, -65, -70, -
                                        75, -80, -85, -90, -95, -100, -110, -120, -130, -140, -150, -160, -170, -180, -190, -200]

                            cp_list = []
                            for i in range(beam_number):
                                cp = df.BeamSequence[i].NumberOfControlPoints
                                cp_list.append(cp)

                            cp_sum = sum(cp_list)

                            tmp_x  = xjaw_position(df, beam_number)
                            xjaw = beamnumber_split(tmp_x, beam_number, cp_list)
                            tmp_sub = list_sub_JTCS(xjaw, df, beam_number)
                            xjaw_sub = beamnumber_split_JTCS(tmp_sub, cp_list, beam_number)
                            xjaw_arc_sum = ARC_sum(xjaw_sub)
                            jtcs_arc = ARC_JTCS(xjaw_arc_sum, df, beam_number)
                            if jtcs_arc == 'None':
                                jtcs = 'None'
                            else:
                                jtcs = sum(jtcs_arc)/beam_number

                            jtcs_data.append(jtcs)
            else:
                jtcs_data.append('算出エラー')

        context['jtcs'] = jtcs_data
        return context

class Mcs(LoginRequiredMixin, ListView):
    model = Rtdatas
    template_name = 'analytics/mcs.html'

    def get_queryset(self):
        query = super().get_queryset()
        region = self.request.GET.get('region', None)
        author = self.request.GET.get('author', None)
        if region:
            query = query.filter(
                region=region
            )
        if author:
            qs = Users.objects.filter(
                username=author
            )
            query = query.filter(
                user_id=qs[0].id
            )
        order_by_create_at = self.request.GET.get('order_by_create_at', 0)
        if order_by_create_at == '1':
            query = query.order_by('create_at')
        elif order_by_create_at == '2':
            query = query.order_by('-create_at')
        return query

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['region'] = self.request.GET.get('region', '')
        context['author'] = self.request.GET.get('author', '')
        order_by_create_at = self.request.GET.get('order_by_create_at', 0)
        if order_by_create_at == '1':
            context['ascending'] = True
        elif order_by_create_at == '2':
            context['descending'] = True

        mcs_data = []
        region = self.request.GET.get('region', None)
        author = self.request.GET.get('author', None)
        if region and author:
            user_id = Users.objects.filter(username=author)
            rtdatas = Rtdatas.objects.filter(region=region, user_id=user_id)
        elif region:
            rtdatas = Rtdatas.objects.filter(region=region)
        elif author:
            user_id = Users.objects.filter(username=author)
            rtdatas = Rtdatas.objects.filter(user_id=user_id)
        else:
            rtdatas = Rtdatas.objects.fetch_all_rtdatas()
        for rtdata in rtdatas:
            rtdata_id = rtdata.id
            plandata = Plandatas.objects.filter(rtdata_id=rtdata_id)
            if plandata.first() is not None:
                        file = Plandatas.objects.get(rtdata_id=rtdata_id)
                        df = pydicom.read_file(file.plandata)
                        if 'FractionGroupSequence' in df :
                            beam_number = df.FractionGroupSequence[0].NumberOfBeams
                            Jaw_ref = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75,
                                    80, 85, 90, 95, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200]
                            Jaw_ref2 = [0, -5, -10, -15, -20, -25, -30, -35, -40, -45, -50, -55, -60, -65, -70, -
                                        75, -80, -85, -90, -95, -100, -110, -120, -130, -140, -150, -160, -170, -180, -190, -200]

                            cp_list = []
                            for i in range(beam_number):
                                cp = df.BeamSequence[i].NumberOfControlPoints
                                cp_list.append(cp)

                            cp_sum = sum(cp_list)

                            tmp_x  = xjaw_position(df, beam_number)
                            tmp_y  = yjaw_position(df, beam_number)
                            tmp_mlc = MLC_position(df, beam_number)
                            tmp_weight = Weight_data(df, beam_number)
                            xjaw = beamnumber_split(tmp_x, beam_number, cp_list)
                            yjaw = beamnumber_split(tmp_y, beam_number, cp_list)
                            mlc = beamnumber_split(tmp_mlc, beam_number, cp_list)
                            mu = MU_data(df, beam_number)
                            total_mu = sum(mu)
                            weight = beamnumber_split(tmp_weight, beam_number, cp_list)
                            tmp_mu_cp = MU_cp(mu, weight, df, beam_number)
                            no_sub_mu_cp = beamnumber_split(tmp_mu_cp, beam_number, cp_list)
                            tmp_list_sub = list_sub(no_sub_mu_cp, df, beam_number)
                            mu_cp = beamnumber_split(tmp_list_sub, beam_number, cp_list)

                            y2jaw = []
                            y1jaw = []
                            for bi in range(beam_number):
                                for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
                                    for jk in range(len(Jaw_ref)):
                                        if Jaw_ref[jk] < yjaw[bi][cj][1] <= Jaw_ref[jk+1]:
                                            y2jaw.append(jk)
                                        if Jaw_ref2[jk] > yjaw[bi][cj][0] >= Jaw_ref2[jk+1]:
                                            y1jaw.append(jk)

                            y1jaw = beamnumber_split(y1jaw, beam_number, cp_list)
                            y2jaw = beamnumber_split(y2jaw, beam_number, cp_list)

                            tmp = []
                            y1_a_bank = []
                            y1_b_bank = []
                            y2_a_bank = []
                            y2_b_bank = []
                            # Y１_Abank(0~30)
                            for bi in range(beam_number):
                                for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
                                    for mk in range(30):
                                        if y1jaw[bi][cj] == mk:
                                            y1_a_bank.append(tmp)
                                            tmp = []
                                            for ml in range(30):
                                                if mk == ml:
                                                    for h in range((29-ml), 30, 1):
                                                        tmp.append(mlc[bi][cj][h])

                            y1_a_bank.append(tmp)
                            y1_a_bank.pop(0)

                            # Y1_Bbank(60~90)
                            for bi in range(beam_number):
                                for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
                                    for mk in range(30):
                                        if y1jaw[bi][cj] == mk:
                                            y1_b_bank.append(tmp)
                                            tmp = []
                                            for ml in range(30):
                                                if mk == ml:
                                                    for h in range((89-ml), 90, 1):
                                                        tmp.append(mlc[bi][cj][h])

                            y1_b_bank.append(tmp)
                            y1_b_bank.pop(0)

                            # Y2_Abank(30~60)
                            for bi in range(beam_number):
                                for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
                                    for mk in range(30):
                                        if y2jaw[bi][cj] == mk:
                                            y2_a_bank.append(tmp)
                                            tmp = []
                                            for ml in range(30):
                                                if mk == ml:
                                                    for h in range(30, (31+ml), 1):
                                                        tmp.append(mlc[bi][cj][h])

                            y2_a_bank.append(tmp)
                            y2_a_bank.pop(0)

                            # Y2_Bbank(90~120)
                            for bi in range(beam_number):
                                for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
                                    for mk in range(30):
                                        if y2jaw[bi][cj] == mk:
                                            y2_b_bank.append(tmp)
                                            tmp = []
                                            for ml in range(30):
                                                if mk == ml:
                                                    for h in range(90, (91+ml), 1):
                                                        tmp.append(mlc[bi][cj][h])

                            y2_b_bank.append(tmp)
                            y2_b_bank.pop(0)

                            # AbankとBbank
                            lsv_a = []
                            lsv_b = []
                            for i in range(cp_sum):
                                lsv_a.append(y1_a_bank[i] + y2_a_bank[i])
                                lsv_b.append(y1_b_bank[i] + y2_b_bank[i])


                            # LSV
                            mlc_a_bank = []
                            mlc_b_bank = []
                            for i in range(cp_sum):
                                mlc_a_bank.append(tmp)
                                tmp = []
                                for j in range(len(lsv_a[i])-1):
                                    a1 = (lsv_a[i][j])
                                    a2 = (lsv_a[i][j+1])
                                    tmp.append(abs(a1-a2))

                            mlc_a_bank.append(tmp)
                            mlc_a_bank.pop(0)

                            for i in range(cp_sum):
                                mlc_b_bank.append(tmp)
                                tmp = []
                                for r in range(len(lsv_b[i])-1):
                                    b1 = (lsv_b[i][r])
                                    b2 = (lsv_b[i][r+1])
                                    tmp.append(abs(b1-b2))

                            mlc_b_bank.append(tmp)
                            mlc_b_bank.pop(0)

                            # Abank & Bbank特徴値取得
                            Asum_Leaf = []
                            Amax_Leaf = []
                            Amin_Leaf = []
                            Asub_Leaf = []
                            Bsum_Leaf = []
                            Bmax_Leaf = []
                            Bmin_Leaf = []
                            Bsub_Leaf = []
                            for i in range(cp_sum):
                                Asum_Leaf.append((y1_a_bank[i])+(y2_a_bank[i]))
                                Amax_Leaf.append(max((Asum_Leaf[i])))
                                Amin_Leaf.append(min((Asum_Leaf[i])))
                                Asub_Leaf.append((Amax_Leaf[i])-(Amin_Leaf[i]))
                                Bsum_Leaf.append((y1_b_bank[i])+(y2_b_bank[i]))
                                Bmax_Leaf.append(max((Bsum_Leaf[i])))
                                Bmin_Leaf.append(min((Bsum_Leaf[i])))
                                Bsub_Leaf.append((Bmax_Leaf[i])-(Bmin_Leaf[i]))

                            sum_list_A = []
                            sum_list_B = []

                            for j in range(cp_sum):
                                list_A = []
                                list_B = []
                                sum_list_A.append(list_A)
                                sum_list_B.append(list_B)
                                for r in range(len(mlc_a_bank[j])):
                                    list_A.append(Asub_Leaf[j]-mlc_a_bank[j][r])
                                for r in range(len(mlc_b_bank[j])):
                                    list_B.append(Bsub_Leaf[j]-mlc_b_bank[j][r])

                            # SUM
                            sum_A = []
                            sum_B = []
                            count_A = []
                            count_B = []

                            for j in range(cp_sum):
                                sum_A.append(sum(sum_list_A[j]))
                                sum_B.append(sum(sum_list_B[j]))
                                count_A.append(len(mlc_a_bank[j]))
                                count_B.append(len(mlc_b_bank[j]))


                            sum_max_A = []
                            sum_max_B = []
                            for j in range(cp_sum):
                                sum_max_A.append(count_A[j]*Asub_Leaf[j])
                                sum_max_B.append(count_B[j]*Bsub_Leaf[j])

                            LSV_A = []
                            LSV_B = []
                            for j in range(cp_sum):
                                LSV_A.append(sum_A[j]/sum_max_A[j])
                                LSV_B.append(sum_B[j]/sum_max_B[j])

                            LSV_CP = []
                            for j in range(cp_sum):
                                LSV_CP.append(LSV_A[j]*LSV_B[j])

                            # AAV
                            y1_a_bank_aav = []
                            y1_b_bank_aav = []
                            y2_a_bank_aav = []
                            y2_b_bank_aav = []
                            cat_y1jaw = []
                            for bi in range(beam_number):
                                for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
                                    cat_y1jaw.append(29 - y1jaw[bi][cj])

                            cat_y1jaw = beamnumber_split(cat_y1jaw, beam_number, cp_list)

                            # Y１_Abank(0~30)
                            for bi in range(beam_number):
                                for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
                                    y1_a_bank_aav.append(tmp)
                                    tmp = []
                                    for r in range(30):
                                        if (cat_y1jaw[bi][cj]) > r:
                                            tmp.append(0)
                                        elif (cat_y1jaw[bi][cj]) == r:
                                            for h in range((30-(30-r)), 30, 1):
                                                tmp.append(mlc[bi][cj][h])
                                        else:
                                            break

                            y1_a_bank_aav.append(tmp)
                            y1_a_bank_aav.pop(0)

                            # Y1_Bbank(60~90)
                            for bi in range(beam_number):
                                for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
                                    y1_b_bank_aav.append(tmp)
                                    tmp = []
                                    for r in range(30):
                                        if cat_y1jaw[bi][cj] > r:
                                            tmp.append(0)
                                        elif cat_y1jaw[bi][cj] == r:
                                            for h in range((89-(29-r)), 90, 1):
                                                tmp.append(mlc[bi][cj][h])
                                        else:
                                            break

                            y1_b_bank_aav.append(tmp)
                            y1_b_bank_aav.pop(0)

                            # Y2_Abank(30~60)
                            for bi in range(beam_number):
                                for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
                                    y2_a_bank_aav.append(tmp)
                                    tmp = []
                                    for r in range(30):
                                        if y2jaw[bi][cj] > r:
                                            pass
                                        elif y2jaw[bi][cj] == r:
                                            for h in range(30, (31+r), 1):
                                                tmp.append(mlc[bi][cj][h])
                                        else:
                                            tmp.append(0)

                            y2_a_bank_aav.append(tmp)
                            y2_a_bank_aav.pop(0)

                            # Y2_Bbank(90~120)
                            for bi in range(beam_number):
                                for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
                                    y2_b_bank_aav.append(tmp)
                                    tmp = []
                                    for r in range(30):
                                        if y2jaw[bi][cj] > r:
                                            pass
                                        elif y2jaw[bi][cj] == r:
                                            for h in range(90, (91+r), 1):
                                                tmp.append(mlc[bi][cj][h])
                                        else:
                                            tmp.append(0)

                            y2_b_bank_aav.append(tmp)
                            y2_b_bank_aav.pop(0)

                            # AbankとBbank
                            lsv_a_aav = []
                            lsv_b_aav = []
                            for i in range(cp_sum):
                                lsv_a_aav.append(y1_a_bank_aav[i] + y2_a_bank_aav[i])
                                lsv_b_aav.append(y1_b_bank_aav[i] + y2_b_bank_aav[i])

                            lsv_a_aav = beamnumber_split(lsv_a_aav, beam_number, cp_list)
                            lsv_b_aav = beamnumber_split(lsv_b_aav, beam_number, cp_list)

                            lsv_a_aav_x = []
                            lsv_b_aav_x = []
                            for bi in range(beam_number):
                                for mk in range(60):
                                    lsv_a_aav_x.append(tmp)
                                    tmp = []
                                    for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
                                        tmp.append(lsv_a_aav[bi][cj][mk])

                            lsv_a_aav_x.append(tmp)
                            lsv_a_aav_x.pop(0)
                            lsv_a_aav_x = mlc_beamnumber_split(lsv_a_aav_x, beam_number)
                            # print(lsv_a_aav_x[0][10])

                            for bi in range(beam_number):
                                for mk in range(60):
                                    lsv_b_aav_x.append(tmp)
                                    tmp = []
                                    for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
                                        tmp.append(lsv_b_aav[bi][cj][mk])

                            lsv_b_aav_x.append(tmp)
                            lsv_b_aav_x.pop(0)
                            lsv_b_aav_x = mlc_beamnumber_split(lsv_b_aav_x, beam_number)

                            lsv_Amin = []
                            lsv_Bmin = []

                            for i in range(beam_number):
                                for j in range(60):
                                    lsv_Amin.append(min(lsv_a_aav_x[i][j]))
                                    lsv_Bmin.append(max(lsv_b_aav_x[i][j]))

                            lsv_Amin = mlc_beamnumber_split(lsv_Amin, beam_number)
                            lsv_Bmin = mlc_beamnumber_split(lsv_Bmin, beam_number)

                            lsv_Amin = np.array(lsv_Amin)
                            lsv_Bmin = np.array(lsv_Bmin)

                            AAV_min = []

                            for i in range(beam_number):
                                for j in range(60):
                                    AAV_min = (lsv_Amin)-(lsv_Bmin)


                            lsv_a = beamnumber_split(lsv_a, beam_number, cp_list)
                            lsv_b = beamnumber_split(lsv_b, beam_number, cp_list)

                            AAV_sub = []
                            for i in range(beam_number):
                                for j in range(df.BeamSequence[i].NumberOfControlPoints):
                                    tmp = []
                                    AAV_sub.append(tmp)
                                    for r in range(len(lsv_a[i][j])):
                                        tmp.append(lsv_a[i][j][r]-lsv_b[i][j][r])

                            sum_AAV = []
                            for ci in range(cp_sum):
                                sum_AAV.append(sum(AAV_sub[ci]))


                            y1_a_bank_aav_out = []
                            y1_b_bank_aav_out = []
                            y2_a_bank_aav_out = []
                            y2_b_bank_aav_out = []

                            # Y１_Abank(0~30)
                            for bi in range(beam_number):
                                for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
                                    y1_a_bank_aav_out.append(tmp)
                                    tmp = []
                                    for r in range(30):
                                        if (cat_y1jaw[bi][cj]) > r:
                                            tmp.append(1000.0)
                                        elif (cat_y1jaw[bi][cj]) == r:
                                            for h in range((30-(30-r)), 30, 1):
                                                tmp.append(mlc[bi][cj][h])
                                        else:
                                            break

                            y1_a_bank_aav_out.append(tmp)
                            y1_a_bank_aav_out.pop(0)

                            # Y1_Bbank(60~90)
                            for bi in range(beam_number):
                                for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
                                    y1_b_bank_aav_out.append(tmp)
                                    tmp = []
                                    for r in range(30):
                                        if cat_y1jaw[bi][cj] > r:
                                            tmp.append(1000.0)
                                        elif cat_y1jaw[bi][cj] == r:
                                            for h in range((89-(29-r)), 90, 1):
                                                tmp.append(mlc[bi][cj][h])
                                        else:
                                            break

                            y1_b_bank_aav_out.append(tmp)
                            y1_b_bank_aav_out.pop(0)

                            # Y2_Abank(30~60)
                            for bi in range(beam_number):
                                for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
                                    y2_a_bank_aav_out.append(tmp)
                                    tmp = []
                                    for r in range(30):
                                        if y2jaw[bi][cj] > r:
                                            pass
                                        elif y2jaw[bi][cj] == r:
                                            for h in range(30, (31+r), 1):
                                                tmp.append(mlc[bi][cj][h])
                                        else:
                                            tmp.append(1000.0)

                            y2_a_bank_aav_out.append(tmp)
                            y2_a_bank_aav_out.pop(0)

                            # Y2_Bbank(90~120)
                            for bi in range(beam_number):
                                for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
                                    y2_b_bank_aav_out.append(tmp)
                                    tmp = []
                                    for r in range(30):
                                        if y2jaw[bi][cj] > r:
                                            pass
                                        elif y2jaw[bi][cj] == r:
                                            for h in range(90, (91+r), 1):
                                                tmp.append(mlc[bi][cj][h])
                                        else:
                                            tmp.append(1000.0)

                            y2_b_bank_aav_out.append(tmp)
                            y2_b_bank_aav_out.pop(0)

                            # AbankとBbank
                            lsv_a_aav_out = []
                            lsv_b_aav_out = []
                            for i in range(cp_sum):
                                lsv_a_aav_out.append(y1_a_bank_aav_out[i] + y2_a_bank_aav_out[i])
                                lsv_b_aav_out.append(y1_b_bank_aav_out[i] + y2_b_bank_aav_out[i])

                            lsv_a_aav_out = beamnumber_split(lsv_a_aav_out, beam_number, cp_list)
                            lsv_b_aav_out = beamnumber_split(lsv_b_aav_out, beam_number, cp_list)

                            aav_sum = []
                            for i in range(beam_number):
                                for j in range(df.BeamSequence[i].NumberOfControlPoints):
                                    aav_sum.append(tmp)
                                    tmp = []
                                    for k in range(60):
                                        if lsv_a_aav_out[i][j][k] == (1000.0):
                                            pass
                                        elif lsv_a_aav_out[i][j][k] != (1000.0):
                                            tmp.append(AAV_min[i][k])
                                aav_sum.append(tmp)
                                aav_sum.pop(0)

                            aav_sum = beamnumber_split(aav_sum, beam_number, cp_list)

                            aav_sum_all = []
                            for i in range(beam_number):
                                for j in range(df.BeamSequence[i].NumberOfControlPoints):
                                    aav_sum_all.append(sum(aav_sum[i][j]))

                            AAV = []
                            for ci in range(cp_sum):
                                AAV.append(sum_AAV[ci]/(aav_sum_all[ci]))

                            AAV = beamnumber_split(AAV, beam_number, cp_list)
                            LSV_CP = beamnumber_split(LSV_CP, beam_number, cp_list)

                            cp_w = []
                            AAV_F = []
                            LSV_F = []

                            for bi in range(beam_number):
                                for cj in range(int(df.BeamSequence[i].NumberOfControlPoints)-1):
                                    AAV_F.append((AAV[bi][cj]+AAV[bi][cj+1])/2)
                                    LSV_F.append((LSV_CP[bi][cj]+LSV_CP[bi][cj+1])/2)
                                    cp_w.append((mu_cp[bi][cj]+mu_cp[bi][cj+1])/mu[bi])

                            AAV_F = cp_beamnumber_split(AAV_F, beam_number, cp_list)
                            LSV_F = cp_beamnumber_split(LSV_F, beam_number, cp_list)
                            cp_w = cp_beamnumber_split(cp_w, beam_number, cp_list)

                            MCS_sum = []
                            for i in range(beam_number):
                                for j in range(int(df.BeamSequence[i].NumberOfControlPoints)-1):
                                    MCS_sum.append(AAV_F[i][j]*LSV_F[i][j]*cp_w[i][j])

                            MCS_sum = cp_beamnumber_split(MCS_sum, beam_number, cp_list)

                            MCS_F = []
                            for i in range(beam_number):
                                MCS_F.append(sum(MCS_sum[i])*(mu[i]/total_mu))

                            MCS = sum(MCS_F)

                            mcs_data.append(MCS)

            else:
                mcs_data.append('算出エラー')

        context['mcs'] = mcs_data
        return context


@login_required
def delete_plandata(request, pk):
    plandata = get_object_or_404(Plandatas, rtdata_id=pk)
    rtdata = get_object_or_404(Rtdatas, pk=pk)
    plandata.delete()
    import os
    if os.path.isfile(plandata.plandata.path):
        os.remove(plandata.plandata.path)
    messages.success(request, 'プランデータを削除しました')
    return redirect('analytics:edit_rtdata', pk=rtdata.id)

@login_required
def delete_stracturedata(request, pk):
    stracturedata = get_object_or_404(Stracturedatas, rtdata_id=pk)
    rtdata = get_object_or_404(Rtdatas, pk=pk)
    stracturedata.delete()
    import os
    if os.path.isfile(stracturedata.stracturedata.path):
        os.remove(stracturedata.stracturedata.path)
    messages.success(request, 'ストラクチャデータを削除しました')
    return redirect('analytics:edit_rtdata', pk=rtdata.id)

@login_required
def delete_ctdata(request, pk, rtdata):
    ctdata = get_object_or_404(Ctdatas, pk=pk)
    rtdata = get_object_or_404(Rtdatas, pk=rtdata)
    ctdata.delete()
    if os.path.isfile(ctdata.ctdata.path):
        os.remove(ctdata.ctdata.path)
    messages.success(request, 'CTデータを削除しました')
    return redirect('analytics:edit_rtdata', pk=rtdata.id)



def post_memo(request, user_id):
    saved_memo = cache.get(f'saved_memo-user_id={request.user.id}', '')
    post_memo_form = forms.PostMemoForm(request.POST or None, initial={'memo': saved_memo})
    memo = Memo.objects.fetch_by_user_id(user_id)
    if user_id != request.user.id:
        raise Http404
    if post_memo_form.is_valid():
        if not request.user.is_authenticated:
            raise Http404
        post_memo_form.instance.user = request.user
        post_memo_form.save()
        cache.delete(f'saved_memo-user_id={request.user.id}')
        return redirect('analytics:post_memo', user_id=user_id)
    return render(
        request, 'analytics/post_memo.html', context={'post_memo_form': post_memo_form, 'memos': memo,}
    )


def save_memo(request):
    if request.is_ajax:
        memo = request.GET.get('memo')
        if memo:
            cache.set(f'saved_memo-user_id={request.user.id}', memo)
            return JsonResponse({'message': '一時保存しました'})

def delete_memo(request, pk):
    memo = get_object_or_404(Memo, id=pk)
    memo.delete()
    messages.success(request, 'メモを削除しました')
    return redirect('analytics:post_memo', user_id=request.user.id)




# def create_rtdata(request):
#     create_rtdata_form = forms.CreateRtdataForm(request.POST or None)
#     if create_rtdata_form.is_valid():
#         create_rtdata_form.instance.user = request.user
#         create_rtdata_form.save()
#         messages.success(request, '照射データを作成しました。')
#         return redirect('analytics:list_rtdatas')
#     return render(
#         request, 'analytics/create_rtdata.html', context={'create_rtdata_form': create_rtdata_form,}
#     )

# def list_rtdatas(request):
#     rtdatas = Rtdatas.objects.fetch_all_rtdatas()
#     return render(request, 'analytics/list_rtdatas.html', context={'rtdatas': rtdatas})

# def edit_rtdata(request, id):
#     rtdata = get_object_or_404(Rtdatas, id=id)
#     if rtdata.user.id != request.user.id:
#         raise Http404
#     edit_rtdata_form = forms.CreateRtdataForm(request.POST or None, instance=rtdata)
#     if edit_rtdata_form.is_valid():
#         edit_rtdata_form.save()
#         messages.success(request, 'RTデータを更新しました')
#         return redirect('analytics:list_rtdatas')
#     return render(
#         request, 'analytics/edit_rtdata.html', context={'edit_rtdata_form': edit_rtdata_form, 'id': id,}
#     )

# def delete_rtdata(request, id):
#     rtdata = get_object_or_404(Rtdatas, id=id)
#     if rtdata.user.id != request.user.id:
#         raise Http404
#     delete_rtdata_form = forms.DeleteRtdataForm(request.POST or None)
#     if delete_rtdata_form.is_valid(): # csrf check
#         rtdata.delete()
#         messages.success(request, 'RTデータを削除しました')
#         return redirect('analytics:list_rtdatas')
#     return render(request, 'analytics/delete_rtdata.html', context={'delete_rtdata_form': delete_rtdata_form})

# def upload_sample(request):
#     if request.method == 'POST' and request.FILES['upload_file']:
#         upload_file = request.FILES['upload_file']
#         fs = FileSystemStorage()
#         file_path = os.path.join('upload', upload_file.name)
#         file = fs.save(file_path, upload_file)
#         uploaded_file_url = fs.url(file)
#         return render(request, 'upload_file.html', context={'uploaded_file_url': uploaded_file_url})
#     return render(request, 'upload_file.html')

# @login_required
# def user(request, id):
#     user2 = get_object_or_404(User, pk=id)
#     # user = User.objects.filter(id=id).first()
#     # if user is None:
#     #     return redirect('Rt_app:users')
#     return render(request, 'user.html', context = {'user': user2})

# @login_required
# def upload_model_form(request):
#     user = None
#     if request.method == 'POST':
#         form = forms.UserForm(request.POST or None, request.FILES or None)
#         if form.is_valid():
#             user = form.save()
#         return redirect('Rt_app:users')
#     else:
#         form = forms.UserForm()
#     return render(request, 'upload_model_form.html', context={'form': form, 'user': user})






# df = pydicom.read_file("RTplan.dcm")  # 取得したいRTplanのファイル名をRTplanにする

# beam_number = df.FractionGroupSequence[0].NumberOfBeams  # Arc数取得

# cp_list = []
# for i in range(beam_number):
#     cp = df.BeamSequence[i].NumberOfControlPoints
#     cp_list.append(cp)

# cp_sum = sum(cp_list)


def beamnumber_split(tosplitdata, beam_number, cp_list):
    '''dataをbeamnumber(Arc数)ごとに分割してListに保存'''

    separate = []
    start = 0
    newArray = []
    for i in range(beam_number):
        if i == 0:
            separate.append(int(cp_list[i]))
            cp = int(cp_list[i])
        else:
            separate.append(cp+int(cp_list[i]))
            cp = cp+int(cp_list[i])
    for sp in separate:
        newArray.append(tosplitdata[start:sp])
        start = sp
    return newArray


def cp_beamnumber_split(tosplitdata, beam_number, cp_list):
    '''dataをbeamnumber(Arc数-1)ごとに分割してListに保存'''

    separate = []
    start = 0
    newArray = []
    for i in range(beam_number):
        if i == 0:
            separate.append(int(cp_list[i])-1)
            cp = int(cp_list[i])-1
        else:
            separate.append(cp+int(cp_list[i])-1)
            cp = cp+int(cp_list[i])-1
    for sp in separate:
        newArray.append(tosplitdata[start:sp])
        start = sp
    return newArray


def mlc_beamnumber_split(tosplitdata, beam_number):
    '''dataをMLCごとに分割してListに保存'''

    separate = []
    start = 0
    newArray = []
    for i in range(beam_number):
        if i == 0:
            separate.append(60)
            mlc = 60
        else:
            separate.append(int(mlc)+60)
            mlc = int(mlc) + 60
    for sp in separate:
        newArray.append(tosplitdata[start:sp])
        start = sp
    return newArray


def xjaw_position(df, beam_number):
    '''Xjawのデータを算出'''

    x_position = []
    for bi in range(beam_number):
        for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
            jaw = df.BeamSequence[bi].ControlPointSequence[cj].BeamLimitingDevicePositionSequence[0].LeafJawPositions
            x_position.append(jaw)
    return x_position


def yjaw_position(df, beam_number):
    '''Yjawのデータを算出'''

    y_position = []
    for bi in range(beam_number):
        for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
            jaw = df.BeamSequence[bi].ControlPointSequence[cj].BeamLimitingDevicePositionSequence[1].LeafJawPositions
            y_position.append(jaw)
    return y_position


def MLC_position(df, beam_number):
    '''MLCデータを算出'''

    mlc_position = []
    for bi in range(beam_number):
        for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
            mlc = df.BeamSequence[bi].ControlPointSequence[cj].BeamLimitingDevicePositionSequence[2].LeafJawPositions
            mlc_position.append(mlc)
    return mlc_position


def MU_data(df, beam_number):
    '''MUデータを算出'''
    mu_data = []
    for bi in range(beam_number):
        MU = df.FractionGroupSequence[0].ReferencedBeamSequence[bi].BeamMeterset
        mu_data.append(MU)
    return mu_data


def Weight_data(df, beam_number):
    '''beam_Weightデータを算出'''

    weight_data = []
    for bi in range(beam_number):
        for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
            weight = df.BeamSequence[bi].ControlPointSequence[cj].CumulativeMetersetWeight
            weight_data.append(weight)
    return weight_data


def MU_cp(mu, weight,df, beam_number):
    '''cp間のMUを算出'''

    mu_cp = []
    for bi in range(beam_number):
        for cj in range(df.BeamSequence[bi].NumberOfControlPoints):
            mu_cp.append(mu[bi]*weight[bi][cj])
    return mu_cp


def list_sub(sub_list, df, beam_number):
    sublist = []
    for bi in range(beam_number):
        for cj in range(int(df.BeamSequence[bi].NumberOfControlPoints)-1):
            sublist.append(sub_list[bi][cj+1] - sub_list[bi][cj])
        sublist.append(0)
    return sublist


def list_sub_JTCS(sub_list, df, beam_number):
    sublist_x1 = []
    sublist_x2 = []
    for bi in range(beam_number):
        for cj in range(int(df.BeamSequence[bi].NumberOfControlPoints)-1):
            sublist_x1.append(abs(sub_list[bi][cj+1][0] - sub_list[bi][cj][0]))
            sublist_x2.append(abs(sub_list[bi][cj+1][1] - sub_list[bi][cj][1]))
    return sublist_x1, sublist_x2


def beamnumber_split_JTCS(tosplitdata,cp_list, beam_number):
    '''dataをbeamnumber(Arc数)ごとに分割してListに保存'''

    separate = []
    newArray = []
    cp_list_JTCS = []
    for i in range(beam_number):
        cp_list_JTCS.append(int(cp_list[i])-1)
    for i in range(beam_number):
        if i == 0:
            separate.append(int(cp_list_JTCS[i]))
            cp = int(cp_list_JTCS[i])
        else:
            separate.append(cp+int(cp_list_JTCS[i]))
            cp = cp+int(cp_list_JTCS[i])
    for i in range(2):
        start = 0
        for sp in separate:
            newArray.append(tosplitdata[i][start:sp])
            start = sp
    return newArray


def ARC_sum(sum_data):
    '''arcごとのデータの合計をリストに保存'''

    Sum_data = []
    for i in range(len(sum_data)):
        Sum_data.append(sum(sum_data[i]))
    return Sum_data


def ARC_JTCS(arc_data,df, beam_number):
    Arc_data = []
    if beam_number == 1:
        return 'None'
    else:
        for i in range(beam_number):
            Arc_data.append((arc_data[i] + arc_data[i+2]) / (int(df.BeamSequence[i].NumberOfControlPoints)-1))
        return Arc_data
