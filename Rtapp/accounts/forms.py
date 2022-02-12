from django import forms
from .models import Users
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class RegistForm(forms.ModelForm):
    username = forms.CharField(label='名前')
    company = forms.CharField(label='会社')
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())

    class Meta:
        model = Users
        fields = ['username','company', 'email', 'password']

    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='メールアドレス') #ログイン時に入力するパラメータ
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    remember = forms.BooleanField(label='ログイン状態を保持する', required=False)

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Users
        fields = ('username', 'email', 'password', 'is_staff', 'is_active', 'is_superuser')

    def clean_password(self):
        # すでに登録されているパスワードを返す
        return self.initial['password']

# *************************************************************************************************************************************

# from django import forms
# from django.contrib.auth.forms import ReadOnlyPasswordHashField
# from matplotlib import widgets
# from pyrsistent import field
# from .models import User
# from django.core.exceptions import ValidationError
# from django.contrib.auth.password_validation import validate_password


# class UserCreationForm(forms.ModelForm):
#     username = forms.CharField(label='名前')
#     email = forms.EmailField(label='メールアドレス')
#     password = forms.CharField(label='パスワード', widget=forms.PasswordInput)
#     confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password')

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get('password')
#         confirm_password = cleaned_data.get('confirm_password')
#         if password != confirm_password:
#             raise ValidationError('パスワードが一致しません')

#     def save(self, commit=False):
#         user = super().save(commit=False)
#         validate_password(self.cleaned_data['password'], user)
#         user.set_password(self.cleaned_data.get("password"))
#         user.save()
#         return user


# class UserChangeForm(forms.ModelForm):
#     password = ReadOnlyPasswordHashField()

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password', 'is_staff', 'is_active', 'is_superuser')

#     def clean_password(self):
#         # すでに登録されているパスワードを返す
#         return self.initial['password']


# class LoginForm(forms.Form):
#     email = forms.CharField(label="メールアドレス")
#     password = forms.CharField(label="パスワード", widget=forms.PasswordInput())

# class UserEditForm(forms.ModelForm):
#     username = forms.CharField(label='名前')
#     email = forms.EmailField(label='メールアドレス')

#     class Meta:
#         model = User
#         fields = ('username', 'email')


# class PasswordChangeForm(forms.ModelForm):

#     password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
#     confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput())

#     class Meta():
#         model = Users
#         fields = ('password', )

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data['password']
#         confirm_password = cleaned_data['confirm_password']
#         if password != confirm_password:
#             raise forms.ValidationError('パスワードが異なります')

#     def save(self, commit=False):
#         user = super().save(commit=False)
#         validate_password(self.cleaned_data['password'], user)
#         user.set_password(self.cleaned_data['password'])
#         user.save()
#         return user

