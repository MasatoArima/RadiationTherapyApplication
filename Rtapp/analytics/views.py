from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from django.contrib import messages
from .models import Rtdatas, Plandatas, Stracturedatas, Ctdatas, Memo
from accounts.models import User
from django.http import Http404
from django.core.cache import cache
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import os

# from turtle import update
# from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
# from django.forms import formset_factory,modelformset_factory
# from fsspec import filesystem
# from matplotlib.style import context
# from psutil import users
# from django.contrib.auth.decorators import login_required


# Create your views here.

def create_rtdata(request):
    create_rtdata_form = forms.CreateRtdataForm(request.POST or None)
    if create_rtdata_form.is_valid():
        create_rtdata_form.instance.user = request.user
        create_rtdata_form.save()
        messages.success(request, '照射データを作成しました。')
        return redirect('analytics:list_rtdatas')
    return render(
        request, 'analytics/create_rtdata.html', context={'create_rtdata_form': create_rtdata_form,}
    )

def list_rtdatas(request):
    rtdatas = Rtdatas.objects.fetch_all_rtdatas()
    return render(request, 'analytics/list_rtdatas.html', context={'rtdatas': rtdatas})

def edit_rtdata(request, id):
    rtdata = get_object_or_404(Rtdatas, id=id)
    if rtdata.user.id != request.user.id:
        raise Http404
    edit_rtdata_form = forms.CreateRtdataForm(request.POST or None, instance=rtdata)
    if edit_rtdata_form.is_valid():
        edit_rtdata_form.save()
        messages.success(request, 'RTデータを更新しました')
        return redirect('analytics:list_rtdatas')
    return render(
        request, 'analytics/edit_rtdata.html', context={'edit_rtdata_form': edit_rtdata_form, 'id': id,}
    )


def delete_rtdata(request, id):
    rtdata = get_object_or_404(Rtdatas, id=id)
    if rtdata.user.id != request.user.id:
        raise Http404
    delete_rtdata_form = forms.DeleteRtdataForm(request.POST or None)
    if delete_rtdata_form.is_valid(): # csrf check
        rtdata.delete()
        messages.success(request, 'RTデータを削除しました')
        return redirect('analytics:list_rtdatas')
    return render(request, 'analytics/delete_rtdata.html', context={'delete_rtdata_form': delete_rtdata_form})



def post_memo(request, user_id):
    saved_memo = cache.get(f'saved_memo-user_id={request.user.id}', '')
    post_memo_form = forms.PostMemoForm(request.POST or None, initial={'memo': saved_memo})
    memo = Memo.objects.fetch_by_user_id(user_id)
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