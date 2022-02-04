from django.shortcuts import render
from django.forms import formset_factory,modelformset_factory
from fsspec import filesystem
from matplotlib.style import context

from .models import ModelSetPost
from . import forms
from django.core.files.storage import FileSystemStorage
import os


# Create your views here.

def home(request):
    form = forms.UserInfo()
    if request.method == 'POST':
        form = forms.UserInfo(request.POST)
        if form.is_valid():
            print('バリデーション成功')
            print(form.cleaned_data)
    return render(request, 'home.html', context = {'form': form})

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

def sample(request):
    name = 'arima masato'
    height = 165.4
    weight = 60
    bmi = weight / (height / 100)**2
    page_url = 'ホームぺージ: https://www.google.com'
    favorite_fruits = ['Apple', 'Grape', 'Lemon']
    msg ="""
    hello
    my name is
    masato
    """
    msg2 = '123456789'
    return render(request, 'sample.html', context={
        'name': name,
        'bmi': bmi,
        'page_url': page_url,
        'fruits': favorite_fruits,
        'msg': msg,
        'msg2': msg2,
    })

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
        form = forms.UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
    else:
        form = forms.UserForm()
    return render(request, 'upload_model_form.html', context={
        'form': form, 'user': user
    })