# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-19 18:03
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    replaces = [('logging_svc', '0001_initial'), ('logging_svc', '0002_auto_20170515_1338'), ('logging_svc', '0003_auto_20170515_1437'), ('logging_svc', '0004_auto_20170519_1737'), ('logging_svc', '0005_auto_20170519_1754')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('hostip', models.GenericIPAddressField(default='0.0.0.0', unpack_ipv4=True)),
                ('hostname', models.CharField(default='nohost', max_length=250, validators=[django.core.validators.RegexValidator(flags=re.RegexFlag(2), regex='^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$')])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Play',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('hostip', models.GenericIPAddressField(default='0.0.0.0', unpack_ipv4=True)),
                ('hostname', models.CharField(default='nohost', max_length=250, validators=[django.core.validators.RegexValidator(flags=re.RegexFlag(2), regex='^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$')])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('hostip', models.GenericIPAddressField(default='0.0.0.0', unpack_ipv4=True)),
                ('hostname', models.CharField(default='nohost', max_length=250, validators=[django.core.validators.RegexValidator(flags=re.RegexFlag(2), regex='^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$')])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
