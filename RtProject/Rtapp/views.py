from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html', context = {'value': 'hello'})

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
    return render(request, 'sample1.html')

def sample2(request):
    return render(request, 'sample2.html')

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
    country = Country('Japan', 1000000, 'Tokyo')
    return render(request, 'sample3.html', context={
        'country': country
    })
