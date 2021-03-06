# Generated by Django 3.2.9 on 2021-11-29 23:33

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('welcome', '0005_auto_20211130_0033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publication_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 30, 0, 33, 17, 989464)),
        ),
        migrations.AlterField(
            model_name='project',
            name='deadline',
            field=models.DateField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='project',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
