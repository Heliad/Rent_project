# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-14 23:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TOFI', '0004_remove_donerent_next_payment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='donerent',
            name='next_payment_date',
            field=models.DateField(default=None),
        ),
    ]