from django.urls import path
from .views import (
    RegistUserView, HomeView, UserLoginView,
    UserLogoutView, UserView
)

app_name = 'accounts'
urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('regist/', RegistUserView.as_view(), name='regist'),
    path('user_login/', UserLoginView.as_view(), name='user_login'),
    path('user_logout/', UserLogoutView.as_view(), name='user_logout'),
    path('user/', UserView.as_view(), name='user'),
]

# *************************************************************************************************************

# from django.urls import path
# from . import views
# from .views import Mypage

# app_name = 'accounts'

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('regist', views.regist, name='regist'),
#     path('activate_user/<uuid:token>', views.activate_user, name='activate_user'),
#     path('user_login', views.user_login, name='user_login'),
#     path('user_logout', views.user_logout, name='user_logout'),
#     path('user_edit', views.user_edit, name='user_edit'),
#     path('change_password', views.change_password, name='change_password'),
#     path('mypage', Mypage.as_view(), name='mypage'),
# ]