# Generated by Django 3.2.9 on 2021-11-29 23:33

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('welcome', '0004_alter_post_publication_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publication_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 30, 0, 33, 4, 144258)),
        ),
        migrations.AlterField(
            model_name='project',
            name='deadline',
            field=models.DateField(blank=True, default=datetime.datetime(2021, 11, 29, 23, 33, 4, 144258, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='project',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2021, 11, 29, 23, 33, 4, 144258, tzinfo=utc)),
        ),
    ]
