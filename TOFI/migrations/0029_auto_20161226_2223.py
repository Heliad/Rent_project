# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-26 19:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('TOFI', '0028_auto_20161226_2122'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercard',
            name='currency_type',
            field=models.CharField(default='BYN', max_length=3),
        ),
    ]