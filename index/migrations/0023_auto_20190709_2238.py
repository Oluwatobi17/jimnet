# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-07-09 21:38
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0022_auto_20190709_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dateofmembership',
            field=models.DateTimeField(default=datetime.datetime(2019, 7, 9, 21, 38, 54, 413835, tzinfo=utc)),
        ),
    ]
