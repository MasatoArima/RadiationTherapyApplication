from django.urls import path
from . import views


app_name = 'Rt_app'
urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('sample1', views.sample1, name='sample1'),
    path('sample2', views.sample2, name='sample2'),
    path('sample3', views.sample3, name='sample3'),
    path('sample4', views.sample4, name='sample4'),
    path('upload_sample', views.upload_sample, name='upload_sample'),
    path('upload_model_form', views.upload_model_form, name='upload_model_form'),
    path('update_user/<int:id>', views.update_user, name='update_user'),
    path('delete_user/<int:id>', views.delete_user, name='delete_user'),
]
