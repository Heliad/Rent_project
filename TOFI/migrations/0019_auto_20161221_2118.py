# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-21 21:18
from __future__ import unicode_literals

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('TOFI', '0018_auto_20161221_2105'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoneRent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_user_renter', models.IntegerField()),
                ('date_rent', models.DateField(default=None)),
                ('payed_until_time', models.FloatField(default=0)),
                ('cost', models.CharField(max_length=50)),
                ('next_payment_date', models.DateField(default=None)),
                ('id_house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TOFI.Rent')),
                ('id_user_owner',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='quickpayment',
            name='username',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE,
                                    to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='quickpayment',
            name='rent',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='TOFI.DoneRent'),
        ),
    ]