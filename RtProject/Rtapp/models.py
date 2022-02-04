import email
from pyexpat import model
from statistics import mode
from venv import create
from django.db import models
from django.utils import timezone
from matplotlib.pyplot import title
import pytz

# Create your models here.

class BaseMeta(models.Model):
    create_at = models.DateTimeField(default=timezone.datetime.now(pytz.timezone('Asia/Tokyo')))
    update_at = models.DateTimeField(default=timezone.datetime.now(pytz.timezone('Asia/Tokyo')))

    class Meta:
        abstract = True #Tableとして作成されないようにする


class Person(BaseMeta): # BaseMetaを継承させている
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birthday = models.DateField(default='1900-01-01')
    email = models.EmailField(db_index=True)
    salary = models.FloatField(null=True)
    memo = models.TextField()
    web_site = models.URLField(null=True, blank=True)

    class Meta:
        db_table = 'Person'
        index_together = [['first_name','last_name']]
        ordering = ['salary']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Students(models.Model):

    name = models.CharField(max_length=20)
    age = models.IntegerField()
    major = models.CharField(max_length=20)
    school = models.ForeignKey(
        'Schools', on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'Students'

    def __str__(self):
        return f'{self.pk},{self.name},{self.age}'

class Schools(models.Model):
    name = models.CharField(max_length=20)
    prefecture = models.ForeignKey(
        'Prefectures', on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'schools'

class Prefectures(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'prefectures'

class Post(models.Model):
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    memo = models.CharField(max_length=255)

class ModelSetPost(models.Model):
    title = models.CharField(max_length=255)
    memo = models.CharField(max_length=255)
    
class User(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    picture = models.FileField(upload_to='picture/%Y/%m/%d')