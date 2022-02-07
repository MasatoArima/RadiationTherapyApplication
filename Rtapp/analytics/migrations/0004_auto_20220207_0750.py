# Generated by Django 3.2.4 on 2022-02-06 22:50

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0003_memo_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='ctdatas',
            name='create_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 6, 22, 50, 36, 368245, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='ctdatas',
            name='update_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 6, 22, 50, 36, 368245, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='memo',
            name='create_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 6, 22, 50, 36, 368245, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='memo',
            name='update_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 6, 22, 50, 36, 368245, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='plandatas',
            name='create_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 6, 22, 50, 36, 368245, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='plandatas',
            name='update_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 6, 22, 50, 36, 368245, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='rtdatas',
            name='create_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 6, 22, 50, 36, 368245, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='rtdatas',
            name='update_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 6, 22, 50, 36, 368245, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='stracturedatas',
            name='create_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 6, 22, 50, 36, 368245, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='stracturedatas',
            name='update_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 6, 22, 50, 36, 368245, tzinfo=utc)),
        ),
    ]