# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-04-12 12:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jimcontrol', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminuser',
            name='pincode',
            field=models.CharField(default='cjmsgf478', max_length=250),
        ),
    ]
