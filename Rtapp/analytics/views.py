from urllib import response
from django.shortcuts import render, redirect, get_object_or_404
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
    # fields = ['region']
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
        print('-'*400)
        print(request.FILES)
        print('-'*400)
        create_rtdata_form = forms.CreateRtdataForm(request.POST or None)
        if create_rtdata_form.is_valid():
            create_rtdata_form.instance.user = request.user
            create_rtdata_form.instance.create_at = datetime.now()
            create_rtdata_form.instance.update_at = datetime.now()
            create_rtdata_form.save()
            rtdata = Rtdatas.objects.order_by("id").last()

        plandata_form = forms.CreatePlandataForm(request.POST or None, request.FILES or None)
        if plandata_form.is_valid(): # リクエストファイルを削除して入力させている。
            plandata_form.save(rtdata=rtdata, plandata=request.FILES['plandata'])

        stracturedata_form = forms.CreateStracturedataForm(request.POST or None, request.FILES or None)
        if stracturedata_form.is_valid():
            stracturedata_form.save(rtdata=rtdata, stracturedata=request.FILES['stracturedata'])

        ctdata_form = forms.CreateCtdataForm(request.POST or None, request.FILES or None)
        if Ctdatas.objects.filter(ctdata='ctdata/' + str(rtdata.pk) + '/'+ str(ctdata_form['ctdata'].data)):
            pass
        elif ctdata_form.is_valid():
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
        # return reverse_lazy('analytics:edit_rtdata', kwargs={'pk': self.object.id})
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
        print('-'*400)
        print(request.FILES)
        print('-'*400)
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


# def upload_sample(request):
#     if request.method == 'POST' and request.FILES['upload_file']:
#         upload_file = request.FILES['upload_file']
#         fs = FileSystemStorage()
#         file_path = os.path.join('upload', upload_file.name)
#         file = fs.save(file_path, upload_file)
#         uploaded_file_url = fs.url(file)
#         return render(request, 'upload_file.html', context={'uploaded_file_url': uploaded_file_url})
#     return render(request, 'upload_file.html')



# def page_not_found(request, exception):
#     return render(request, '404.html', status=404)

# def server_error(request):
#     return render(request, '500.html', status=500)

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