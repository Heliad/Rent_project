# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-15 01:13
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('TOFI', '0005_donerent_next_payment_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='autopayment',
            name='id_rent',
        ),
        migrations.RemoveField(
            model_name='autopayment',
            name='user_id',
        ),
        migrations.AddField(
            model_name='autopayment',
            name='next_payment_date',
            field=models.DateField(default=None),
        ),
        migrations.AddField(
            model_name='autopayment',
            name='payment_interval',
            field=models.IntegerField(default=30),
        ),
        migrations.AlterField(
            model_name='autopayment',
            name='id_quick_payment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TOFI.QuickPayment'),
        ),
    ]
