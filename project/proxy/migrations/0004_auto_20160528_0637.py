# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-28 06:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proxy', '0003_auto_20160527_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proxy',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
