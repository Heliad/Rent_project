# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-08 23:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TOFI', '0046_donepenalty'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donepenalty',
            name='size_penalty',
            field=models.FloatField(),
        ),
    ]