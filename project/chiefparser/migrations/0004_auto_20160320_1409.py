# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-20 14:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chiefparser', '0003_auto_20160320_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='energy_val',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='chiefparser.EnergyValue'),
        ),
    ]
