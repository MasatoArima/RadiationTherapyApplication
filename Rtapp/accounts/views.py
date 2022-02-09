from urllib import request
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from .forms import RegistForm, UserLoginForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from datetime import datetime
from .models import Users
from analytics.models import Rtdatas
from urllib.parse import quote


def top(request):
    return redirect('accounts:home')

class HomeView(TemplateView):
    template_name = 'accounts/home.html'

class RegistUserView(CreateView):
    template_name = 'accounts/regist.html'
    form_class = RegistForm


# ログイン後メッセージを表示させる
class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    authentication_form = UserLoginForm

    def form_valid(self, form):
        remember = form.cleaned_data['remember']
        if remember:
            self.request.session.set_expiry(86400) # (一日)
        return super().form_valid(form)

class UserLogoutView(LogoutView):
    pass

class UserView(LoginRequiredMixin, DetailView):
    model = Users
    template_name = 'accounts/user.html'

    # def dispatch(self, *args, **kwargs):
    #     return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time'] = datetime.now()
        user = self.request.user
        context['rtdatas'] = Rtdatas.objects.filter(user_id = user).order_by('region')
        return context

def handler400(request, exception):
    return render(request, 'errors/400.html', {}, status=400)

def handler403(request, exception):
    return render(request, 'errors/403.html', {}, status=403)

def handler404(request, exception):
    context = {"request_path": quote(request.path)}
    return render(request, 'errors/404.html', context, status=404)

def handler500(request):
    return render(request, 'errors/500.html', {}, status=500)


# ********************************************************************************************************************************

# from tracemalloc import get_object_traceback
# from django.shortcuts import render, redirect, get_object_or_404
# from . import forms
# from django.core.exceptions import ValidationError

# from .models import UserActivateTokens, User
# from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import update_session_auth_hash
# from django.views.generic.base import(View,)

# # Create your views here.

# def top(request):
#     return redirect('accounts:home')

# def home(request):
#     return render(request, 'accounts/home.html')

# def regist(request):
#     regist_form = forms.UserCreationForm(request.POST or None)
#     if regist_form.is_valid():
#         try:
#             regist_form.save()
#             return redirect('accounts:home')
#         except ValidationError as e:
#             regist_form.add_error('password', e)
#     return render(request, 'accounts/regist.html', context={'regist_form': regist_form,})

# def activate_user(request, token):
#     user_activate_token = UserActivateTokens.objects.activate_user_by_token(token)
#     return render(
#         request, 'accounts/activate_user.html'
#     )

# def user_login(request):
#     login_form = forms.LoginForm(request.POST or None)
#     if login_form.is_valid():
#         email = login_form.cleaned_data.get('email')
#         password = login_form.cleaned_data.get('password')
#         user = authenticate(email=email, password=password)
#         if user:
#             if user.is_active:
#                 login(request, user)
#                 messages.success(request, 'ログイン完了しました。')
#                 return redirect('accounts:home')
#             else:
#                 messages.warning(request, 'ユーザがアクティブでありません')
#         else:
#             messages.warning(request, 'メールアドレスかパスワードが間違っています')
#     return render(
#         request, 'accounts/user_login.html', context={
#             'login_form': login_form,
#         }
#     )


# @login_required
# def user_logout(request):
#     logout(request)
#     messages.success(request, 'ログアウトしました')
#     return redirect('accounts:home')

# @login_required
# def user_edit(request):
#     user_edit_form = forms.UserEditForm(request.POST or None, request.FILES or None, instance=request.user)
#     if user_edit_form.is_valid():
#         messages.success(request, '更新完了しました。')
#         user_edit_form.save()
#     return render(request, 'accounts/user_edit.html', context={
#         'user_edit_form': user_edit_form,
#     })

# @login_required
# def change_password(request):
#     password_change_form = forms.PasswordChangeForm(request.POST or None, instance=request.user)
#     if password_change_form.is_valid():
#         try:
#             password_change_form.save()
#             messages.success(request, 'パスワード更新完了しました。')
#             update_session_auth_hash(request, request.user)
#         except ValidationError as e:
#             password_change_form.add_error('password', e)
#     return render(
#         request, 'accounts/change_password.html', context={
#             'password_change_form': password_change_form,
#         }
#     )

# # classベース
# class Mypage(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'accounts/mypage.html')


