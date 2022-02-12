from django.contrib import admin

# Register your models here.


#  ************************************************************************************
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .forms import UserChangeForm, RegistForm
# from .models import Students, Schools

User = get_user_model()

class CustomizeUserAdmin(UserAdmin):
    form = UserChangeForm # ユーザ編集画面でつかうForm
    add_form = RegistForm # ユーザ作成画面

    # 一覧画面で表示する
    list_display = ('username', 'email', 'is_staff')

    # ユーザ編集画面で表示する要素
    fieldsets = (
        ('ユーザ情報', {'fields': ('username', 'email', 'password')}),
        ('パーミッション', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )

    add_fieldsets = (
        ('ユーザ情報', {
            'fields': ('username', 'email', 'password', 'confirm_password')
        }),
    )


admin.site.register(User, CustomizeUserAdmin)