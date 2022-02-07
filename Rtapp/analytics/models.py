from django.db import models
from django.utils import timezone
import pytz

# import logging
# application_logger = logging.getLogger('application-logger')


class BaseModel(models.Model):
    create_at = models.DateTimeField(default=timezone.datetime.now(pytz.timezone('Asia/Tokyo')))
    update_at = models.DateTimeField(default=timezone.datetime.now(pytz.timezone('Asia/Tokyo')))

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

    def __str__(self):
        return  self.region

class Plandatas(BaseModel):
    rtdata = models.OneToOneField(
        Rtdatas,
        on_delete=models.CASCADE,
        primary_key=True
    )

    name = models.CharField(max_length=10)

    class Meta:
        db_table = 'plandata'
        verbose_name_plural = 'プランデータ'

    def __str__(self):
        return  self.name


class Stracturedatas(BaseModel):
    rtdata = models.OneToOneField(
        Rtdatas,
        on_delete=models.CASCADE,
        primary_key=True
    )

    name = models.CharField(max_length=10)

    class Meta:
        db_table = 'stracturedatas'
        verbose_name_plural = 'ストラクチャデータ'

    def __str__(self):
        return  self.name



class Ctdatas(BaseModel):
    rtdata = models.OneToOneField(
        Rtdatas,
        on_delete=models.CASCADE,
        primary_key=True
    )

    name = models.CharField(max_length=10)

    class Meta:
        db_table = 'ctdatas'
        verbose_name_plural = 'CTデータ'

    def __str__(self):
        return  self.name




class MemoManager(models.Manager):
    def fetch_by_user_id(self, user_id):
        return self.filter(user_id=user_id).order_by('id').all()

class Memo(BaseModel):

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