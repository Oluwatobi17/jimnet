# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-04-17 12:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0011_auto_20190417_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dateofmembership',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 17, 12, 13, 40, 462422, tzinfo=utc)),
        ),
    ]