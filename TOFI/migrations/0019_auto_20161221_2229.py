# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-21 19:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TOFI', '0018_sessionkeys'),
    ]

    operations = [
        migrations.AddField(
            model_name='logoperationsbalance',
            name='amount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='logoperationsbalance',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
