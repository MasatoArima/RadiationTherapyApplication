from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.urls import reverse_lazy


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Enter Email')
        user = self.model(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.model(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def get_absolute_url(self):
        return reverse_lazy('accounts:home')

    def __str__(self):
        return self.username

# ********************************************************************************************************************************

# from email.policy import default
# from tabnanny import verbose
# from django.db import models
# from django.contrib.auth.models import ( BaseUserManager, AbstractBaseUser, PermissionsMixin)
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from uuid import uuid4
# from datetime import datetime, timedelta
# from django.contrib.auth.models import UserManager

# class UserManager(BaseUserManager):

#     def create_user(self, username, email, password=None):
#         if not email:
#             raise ValueError('Enter Email!')
#         user = self.model(
#             username=username,
#             email=email
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, email, password=None):
#         user = self.model(
#             username=username,
#             email=email,
#         )
#         user.set_password(password)
#         user.is_staff = True
#         user.is_active = True
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user


# class User(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(max_length=150)
#     email = models.EmailField(max_length=255, unique=True)
#     is_active = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)

#     USERNAME_FIELD = 'email' # このテーブルのレコードを一意に識別
#     REQUIRED_FIELDS = ['username'] # スーパーユーザ作成時に入力する

#     objects = UserManager()

#     def __str__(self):
#         return self.username

#     class Meta:
#         verbose_name_plural = '登録ユーザー'


# class UserActivateTokensManager(models.Manager):

#     def activate_user_by_token(self, token):
#         user_activate_token = self.filter(
#             token=token,
#             expired_at__gte=datetime.now()
#         ).first()
#         user = user_activate_token.user
#         user.is_active = True
#         user.save()

# class UserActivateTokens(models.Model):

#     token = models.UUIDField(db_index=True)
#     expired_at = models.DateTimeField()
#     user = models.ForeignKey(
#         'User', on_delete=models.CASCADE
#     )

#     objects = UserActivateTokensManager()

#     class Meta:
#         db_table = 'user_activate_tokens'

# @receiver(post_save, sender=User)
# def publish_token(sender, instance, **kwargs):
#     user_activate_token = UserActivateTokens.objects.create(
#         user=instance, token=str(uuid4()), expired_at=datetime.now() + timedelta(days=1)
#     )
#     # メールでURLを送る方がよい-------------------------------------------------------------------------------
#     print(f'http://127.0.0.1:8000/accounts/activate_user/{user_activate_token.token}')
#     # ---------------------------------------------------------------------------------------------------------