# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-06-28 05:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('jimcontrol', '0009_auto_20190613_0517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminnotification',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 28, 5, 13, 22, 558050, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='adminuser',
            name='email',
            field=models.EmailField(default='jhawwal@yahoo.com', max_length=500),
        ),
    ]
