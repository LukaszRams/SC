# Generated by Django 3.2.9 on 2021-12-20 21:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('welcome', '0008_auto_20211218_2230'),
    ]

    operations = [
        migrations.AddField(
            model_name='club',
            name='token',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='post',
            name='publication_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 12, 20, 22, 43, 53, 940522)),
        ),
    ]
