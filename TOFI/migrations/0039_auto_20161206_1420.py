# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-06 11:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TOFI', '0038_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='currency_value',
            field=models.FloatField(),
        ),
    ]
