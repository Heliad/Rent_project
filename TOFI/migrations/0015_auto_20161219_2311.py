# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-19 20:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TOFI', '0014_auto_20161217_2321'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='wrong_password_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='date',
            field=models.DateField(default=None, verbose_name='Дата подачи жалобы:'),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='describe',
            field=models.CharField(max_length=150, verbose_name='Текст жалобы:'),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='login_user_from',
            field=models.CharField(max_length=100, verbose_name='От кого жалоба:'),
        ),
        migrations.AlterField(
            model_name='complaint',
            name='login_user_to',
            field=models.CharField(max_length=100, verbose_name='На кого жалоба:'),
        ),
    ]