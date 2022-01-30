from distutils.command.build_scripts import first_line_re
import os
from turtle import update
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RtProject.settings')
from django import setup
setup()

from Rtapp.models import Person

persons = Person.objects.all()
for person in persons:
    print(person.id, person, person.salary)

person = Person.objects.get(pk=1)
print(person.id, person)

#filter(絞り込み、エラーにならない、複数取得可)
persons = Person.objects.filter(first_name = 'taro').all()
print(persons)

for person in persons:
    print(person.id, person, person.salary)


# データ更新
from django.utils import timezone
import pytz

person = Person.objects.get(id=1)
print(person)
person.birthday = '2222-01-01'
person.save()

persons =Person.objects.filter(first_name='taro')
for person in persons:
    person.first_name = 'person.first_name.upper()'
    person.update_at = timezone.datetime.now(pytz.timezone('Asia/Tokyo'))
    # person.save()


Person.objects.filter(first_name='ari').update(
    memo = 'update',
    update_at = timezone.datetime.now(pytz.timezone('Asia/Tokyo'))
)


# データ削除(filterやallでデータ取得後に削除)
Person.objects.filter(first_name='test').delete()