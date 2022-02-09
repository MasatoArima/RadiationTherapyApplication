from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help='ユーザ情報を表示するバッチです'

    # def add_arguments(self, parser):
    #     parser.add_argument('name', type=str, help='名前') # 1引数
    #     parser.add_argument('age', type=int) # 2引数
    #     parser.add_argument('--birthday', default='2020-01-01')
    #     parser.add_argument('three_words', nargs=3)
    #     parser.add_argument('--active', action='store_true')
    #     parser.add_argument('--color', choices=['Blue', 'Red', 'Yellow'])

    def handle(self, *args, **options):
        print('バッチ処理')