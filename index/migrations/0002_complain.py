# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-04-12 12:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jimcontrol', '0002_auto_20190412_1344'),
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=1000)),
                ('email', models.EmailField(max_length=200)),
                ('subject', models.CharField(max_length=500)),
                ('msgstatus', models.BooleanField(default=False)),
                ('date', models.DateTimeField(default=datetime.datetime(2019, 4, 12, 13, 44, 16, 308290))),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jimcontrol.Staff')),
            ],
        ),
    ]