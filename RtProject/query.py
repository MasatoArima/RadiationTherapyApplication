from ctypes import Structure
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RtProject.settings')
from django import setup
setup()

# モデルimport
from Rtapp.models import Students, Person, Schools

# 全権取得
Students.objects.all()

# 頭5権取得
Students.objects.all()[:5]

# 5件目より後
Students.objects.all()[5:]

# 5~7件目
Students.objects.all()[5:8]

# クエリ確認法
Students.objects.all()[5:8].query

# 最初の一件
Students.objects.first()

# 同じもののみ
Students.objects.filter(name='太郎')
Students.objects.filter(age=17)

# AND条件
Students.objects.filter(name='太郎', pk__gt=13).query
Students.objects.filter(name='太郎', pk__lt=13).query

# 前方一致
Students.objects.filter(name__startswith='太')

# 後方一致
Students.objects.filter(name__endswith='郎')

# OR文
from django.db.models import Q
Students.objects.filter(Q(name='太郎')|Q(pk__gt=19))


# IN
ids = [13,14,15]
Students.objects.filter(pk__in=ids)

# 部分一致
Students.objects.filter(name__contains='三')

# is null
Person.objects.filter(salary__isnull=True)
Person.objects.exclude(salary__isnull=True)

Students.objects.exclude(name='太郎')

# values 一部のカラムのみ取得
Students.objects.values('name','age')
Students.objects.values('name','age').filter(pk=14)

# order_by
Students.objects.order_by('-id')

# 集計
from django.db.models import Max, Min, Avg, Count, Sum
Students.objects.count()
Students.objects.filter(name='太郎').count()
Students.objects.aggregate(Count('pk'), Max('pk'), Min('pk'), Avg('pk'), 合計値=Sum('pk'))

# GROUP BY
Students.objects.values('name').annotate(
    Max('pk'), Min('pk')
)
Students.objects.values('name','age').annotate(
    test1=Max('pk'), test2=Min('pk')
)

# 外部キーでフィルター
for student in Students.objects.filter(school__name='南高校'):
    print(student.name, student.school.name, student.school.prefecture.name)

for student in Students.objects.exclude(school__name='南高校'):
    print(student.name, student.school.name, student.school.prefecture.name)

# GROUP BY
for student in Students.objects.order_by('-school__name'):
    print(student.name, student.school.name)

Students.objects.values('school__name').annotate(
    Count('id'), Max('id'), Min('id'), Avg('id'), 合計値=Sum('id')
)
