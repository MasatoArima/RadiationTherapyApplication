from django.core.management.base import BaseCommand
from analytics.models import Rtdatas
from Rtapp.settings import BASE_DIR
from datetime import datetime
import os
import csv



class Command(BaseCommand):
    '''
    全件取得 : python manage.py export_datas
    user_id取得 : python manage.py export_data --user_id 1
    '''

    def add_arguments(self, parser):
        parser.add_argument('--user_id', default='all')

    def handle(self, *args, **options):
        rtdatas = Rtdatas.objects
        user_id = options['user_id']
        if user_id == 'all':
            rtdatas = rtdatas.all()
        else:
            rtdatas = rtdatas.filter(user_id=user_id)
        file_path = os.path.join(BASE_DIR, 'output', 'rtdatas', f'rtdatas_{datetime.now().strftime("%Y%m%d%H%M%S")}_{user_id}')
        with open(file_path, mode='w', newline='\n', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'region', 'test']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for rtdata in rtdatas:
                writer.writerow({
                    'id': rtdata.id,
                    'region': rtdata.region,
                    'test': rtdata.plandatas.plandata
                })