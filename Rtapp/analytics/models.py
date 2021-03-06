from django.db import models
from django.utils import timezone
import pytz
from django.urls import reverse_lazy
import os
# import logging
# application_logger = logging.getLogger('application-logger')


class BaseModel(models.Model):
    # create_at = models.DateTimeField(default=timezone.datetime.now(pytz.timezone('Asia/Tokyo')))
    # update_at = models.DateTimeField(default=timezone.datetime.now(pytz.timezone('Asia/Tokyo')))
    create_at = models.DateTimeField()
    update_at = models.DateTimeField()

    class Meta:
        abstract = True #Tableとして作成されないようにする

class RtdatasManager(models.Manager):

    def fetch_all_rtdatas(self):
        return self.order_by('id').all()

class Rtdatas(BaseModel):
    region = models.CharField(max_length=10)
    user = models.ForeignKey(
        'accounts.Users', on_delete=models.CASCADE
    )

    objects = RtdatasManager()

    class Meta:
        db_table = 'rtdata'
        verbose_name_plural = 'RTデータ'

    def get_absolute_url(self):
        return reverse_lazy('analytics:detail_rtdata', kwargs={'pk': self.pk})

    def __str__(self):
        return  self.region

class PlandatasManager(models.Manager):
    def filter_by_rtdata(self, rtdata):
        return self.filter(rtdata=rtdata).all()

class Plandatas(BaseModel):
    plandata = models.FileField(upload_to='plandata/')
    rtdata = models.OneToOneField(
        Rtdatas,
        on_delete=models.CASCADE,
        primary_key=True
    )
    objects = PlandatasManager()

    class Meta:
        db_table = 'plandatas'
        verbose_name_plural = 'プランデータ'

class StracturedatasManager(models.Manager):
    def filter_by_rtdata(self, rtdata):
        return self.filter(rtdata=rtdata).all()

class Stracturedatas(BaseModel):
    stracturedata = models.FileField(upload_to='stracturedata/')
    rtdata = models.OneToOneField(
        Rtdatas,
        on_delete=models.CASCADE,
        primary_key=True
    )
    objects = StracturedatasManager()

    class Meta:
        db_table = 'stracturedatas'
        verbose_name_plural = 'ストラクチャデータ'

class CtdatasManager(models.Manager):
    def filter_by_rtdata(self, rtdata):
        return self.filter(rtdata=rtdata).all()

class Ctdatas(BaseModel):

    rtdata  = models.ForeignKey(
        'Rtdatas', on_delete=models.CASCADE
    )

    def file_upload_path(instance, filename):
        ext = filename
        new_name = instance.rtdata.id
        return f'ctdata/{new_name}/{ext}'

    ctdata = models.FileField(upload_to=file_upload_path)

    objects = CtdatasManager()

    class Meta:
        db_table = 'ctdatas'
        verbose_name_plural = 'CTデータ'





class MemoManager(models.Manager):
    def fetch_by_user_id(self, user_id):
        return self.filter(user_id=user_id).order_by('id').all()

class Memo(models.Model):

    title = models.CharField(max_length=100, null=True)
    memo = models.CharField(max_length=1000)
    user = models.ForeignKey(
        'accounts.Users', on_delete=models.CASCADE
    )

    objects = MemoManager()

    class Meta:
        db_table = 'memo'



# class FileUpload(models.Model):
#     upload = models.FileField(upload_to='file/%Y/%m/%d')