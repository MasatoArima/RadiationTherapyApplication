from turtle import update
from django.shortcuts import render
from django.forms import formset_factory,modelformset_factory
from fsspec import filesystem
from matplotlib.style import context
from psutil import users

from .models import ModelSetPost, User
from . import forms
from django.core.files.storage import FileSystemStorage
import os


# Create your views here.

def home(request):
    users = User.objects.all()
    return render(request, 'home.html', context={'users': users})

def about(request):
    my_name = 'masato arima'
    favorite_fruits = ['Apple', 'Grape', 'Lemon']
    my_info = {
        'name' : 'masato',
        'age': 29
    }
    status = 20
    return render(request, 'about.html', context = {
        'my_name': my_name,
        'favorite_fruits': favorite_fruits,
        'my_info': my_info,
        'status': status,
    })

def sign_up(request):
    form = forms.UserInfo()
    if request.method == 'POST':
        form = forms.UserInfo(request.POST)
        if form.is_valid():
            print('バリデーション成功')
            print(form.cleaned_data)
    return render(request, 'sign_up.html', context = {'form': form})


def sample1(request):
    form = forms.PostModelForm()
    if request.method == 'POST':
        form = forms.PostModelForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'sample1.html', context = {'form': form})

def sample2(request):
    form = forms.PostModelForm()
    if request.method == 'POST':
        form = forms.PostModelForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'sample2.html', context = {'form': form})


class Country:

    def __init__(self, name, population, capital):
        self.name = name
        self.population = population
        self.capital = capital

def sample3(request):
    TestFormset = formset_factory(forms.FormSetPost, extra=3)
    formset = TestFormset(request.POST or None)
    if formset.is_valid():
        for form in formset:
            print(form.cleaned_data)
    return render(
        request, 'sample3.html', context={'formset': formset}
    )

def sample4(request):
    # TestFormSet = modelformset_factory(ModelSetPost, fields='__all__', extra=3)
    TestFormSet = modelformset_factory(ModelSetPost, form=forms.ModelFormSetPost, extra=3)
    formset = TestFormSet(request.POST or None, queryset=ModelSetPost.objects.filter(id__gt=3))
    if formset.is_valid():
        formset.save()
    return render(
        request, 'sample4.html', context={'formset': formset}
    )

def upload_sample(request):
    if request.method == 'POST' and request.FILES['upload_file']:
        upload_file = request.FILES['upload_file']
        fs = FileSystemStorage()
        file_path = os.path.join('upload', upload_file.name)
        file = fs.save(file_path, upload_file)
        uploaded_file_url = fs.url(file)
        return render(request, 'upload_file.html', context={'uploaded_file_url': uploaded_file_url})
    return render(request, 'upload_file.html')

def upload_model_form(request):
    user = None
    if request.method == 'POST':
        form = forms.UserForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            user = form.save()
    else:
        form = forms.UserForm()
    return render(request, 'upload_model_form.html', context={
        'form': form, 'user': user
    })

def update_user(request, id):
    user = User.objects.get(id=id)
    update_form = forms.UserUpdateForm(
        initial = {
            'name': user.name, 'age': user.age, 'picture': user.picture
        }
    )
    if request.method =='POST':
        update_form = forms.UserUpdateForm(request.POST or None, request.FILES or None)
        if update_form.is_valid():
            user.name = update_form.cleaned_data['name']
            user.age = update_form.cleaned_data['age']
            picture = update_form.cleaned_data['picture']
            if picture:
                fs = FileSystemStorage()
                file_name = fs.save(os.path.join('user', picture.name), picture)
                user.picture = file_name
            user.save()
    return render(
        request, 'update_user.html', context={'user': user, 'update_form': update_form}
    )

def delete_user(request, id):
    delete_form = forms.UserDeleteForm(
        initial = {
            'id':id
        }
    )
    if request.method == 'POST':
        delete_form = forms.UserDeleteForm(request.POST or None)
        if delete_form.is_valid():
            User.objects.get(id=delete_form.cleaned_data['id']).delete()
    return render(
        request, 'delete_user.html', context={'delete_form':delete_form}
    )