# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-05 20:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TOFI', '0035_auto_20161205_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quickpayment',
            name='user_payment',
            field=models.CharField(default=None, max_length=50),
        ),
    ]