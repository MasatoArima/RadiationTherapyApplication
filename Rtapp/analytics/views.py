from urllib import response
from django.shortcuts import render, redirect, get_object_or_404
from matplotlib.style import context
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
from matplotlib.style import context

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

        context['jtcs'] = jtcs_data
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
