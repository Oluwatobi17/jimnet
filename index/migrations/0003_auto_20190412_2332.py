# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-04-12 22:32
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_complain'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complain',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 12, 23, 32, 9, 63147)),
        ),
    ]
