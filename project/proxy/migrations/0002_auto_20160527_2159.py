# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-27 21:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proxy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proxy',
            name='proxy_ip',
            field=models.CharField(max_length=20),
        ),
    ]
