
# 初期データ作成

# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Rtapp.settings')
# from django import setup
# setup()

# from account.models import user

# p = Person(
#     first_name = 'taro',
#     last_name = 'sato',
#     birthday = '2000-01-01',
#     email = 'aa@test.com',
#     salary = 10000,
#     memo = '',
#     web_site = 'http://www.com'
# )
# # p.save()

# # classmetod create

# # Person.objects.create(
# #     first_name = 'test',
# #     last_name = 'test',
# #     birthday = '2000-01-01',
# #     email = 'aa@test.com',
# #     salary = 10000,
# #     memo = 'classmethod実行',
# #     web_site = None
# # )

# # get_or_create(取得 or 作成)
# obj, created = Person.objects.get_or_create(
#     first_name = 'ari',
#     last_name = 'masa',
#     birthday = '2000-01-01',
#     email = 'aa@test.com',
#     salary = 10000,
#     memo = 'classmethod実行',
#     web_site = None
# )

# print(obj)
# print(created)