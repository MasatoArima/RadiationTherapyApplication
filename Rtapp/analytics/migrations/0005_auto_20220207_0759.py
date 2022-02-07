# Generated by Django 3.2.4 on 2022-02-06 22:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0004_auto_20220207_0750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ctdatas',
            name='create_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 6, 22, 59, 57, 207906, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='ctdatas',
            name='update_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 6, 22, 59, 57, 207906, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='memo',
            name='create_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 6, 22, 59, 57, 207906, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='memo',
            name='update_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 6, 22, 59, 57, 207906, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='plandatas',
            name='create_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 6, 22, 59, 57, 207906, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='plandatas',
            name='update_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 6, 22, 59, 57, 207906, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='rtdatas',
            name='create_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 6, 22, 59, 57, 207906, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='rtdatas',
            name='update_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 6, 22, 59, 57, 207906, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='stracturedatas',
            name='create_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 6, 22, 59, 57, 207906, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='stracturedatas',
            name='update_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 6, 22, 59, 57, 207906, tzinfo=utc)),
        ),
    ]
