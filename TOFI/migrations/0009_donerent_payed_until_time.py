# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-16 00:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('TOFI', '0008_complaint'),
    ]

    operations = [
        migrations.AddField(
            model_name='donerent',
            name='payed_until_time',
            field=models.IntegerField(default=0),
        ),
    ]