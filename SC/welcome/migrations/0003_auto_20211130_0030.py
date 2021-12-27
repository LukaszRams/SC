# Generated by Django 3.2.9 on 2021-11-29 23:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('welcome', '0002_auto_20211130_0026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publication_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 30, 0, 30, 42, 61936)),
        ),
        migrations.AlterField(
            model_name='project',
            name='deadline',
            field=models.DateField(blank=True, default=datetime.date(2021, 11, 30)),
        ),
        migrations.AlterField(
            model_name='project',
            name='start_date',
            field=models.DateField(default=datetime.date(2021, 11, 30)),
        ),
    ]
