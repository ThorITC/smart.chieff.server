# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-23 06:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chiefparser', '0006_auto_20160323_0615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='cooking_time',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
