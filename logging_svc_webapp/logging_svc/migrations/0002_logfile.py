# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-25 17:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logging_svc', '0001_squashed_0005_auto_20170519_1754'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_file', models.FileField(upload_to='')),
            ],
        ),
    ]
