# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-26 12:21
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('TOFI', '0025_auto_20161222_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quickpayment',
            name='user_payment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TOFI.UserCard'),
        ),
    ]
