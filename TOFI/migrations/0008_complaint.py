# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-15 13:28
from __future__ import unicode_literals

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
                ('login_user_from', models.CharField(max_length=100, verbose_name='От кого жалоба')),
                ('login_user_to', models.CharField(max_length=100, verbose_name='На кого жалоба')),
                ('describe', models.CharField(max_length=150, verbose_name='Текаст жалобы')),
                ('date', models.DateField(default=None, verbose_name='Дата подачи жалобы')),
            ],
        ),
    ]