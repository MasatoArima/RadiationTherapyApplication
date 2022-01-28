from django.urls import path
from . import views

app_name = 'Rt_app'
urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('sample1', views.sample1, name='sample1'),
    path('sample2', views.sample2, name='sample2'),
    path('sample', views.sample, name='sample'),
    path('sample3', views.sample3, name='sample3'),
]
