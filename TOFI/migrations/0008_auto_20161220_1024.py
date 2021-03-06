# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-20 10:24
from __future__ import unicode_literals

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('TOFI', '0007_auto_20161215_0113'),
    ]

    operations = [
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_user_from', models.CharField(max_length=100, verbose_name='От кого жалоба:')),
                ('login_user_to', models.CharField(max_length=100, verbose_name='На кого жалоба:')),
                ('describe', models.CharField(max_length=150, verbose_name='Текст жалобы:')),
                ('date', models.DateField(default=None, verbose_name='Дата подачи жалобы:')),
            ],
        ),
        migrations.AddField(
            model_name='donerent',
            name='payed_until_time',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='donerent',
            name='id_house',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TOFI.Rent'),
        ),
        migrations.AlterField(
            model_name='donerent',
            name='id_user_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='quickpayment',
            name='amount',
            field=models.FloatField(default=None),
        ),
        migrations.AlterField(
            model_name='rent',
            name='user_login',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
