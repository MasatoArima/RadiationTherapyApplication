from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help='ユーザ情報を表示するバッチです'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='名前') # 1引数
        parser.add_argument('--active', action='store_true')
        parser.add_argument('--color', choices=['Blue', 'Red', 'Yellow'])

    def handle(self, *args, **options):
        name = options['name']
        print(name)
        print('バッチ処理')