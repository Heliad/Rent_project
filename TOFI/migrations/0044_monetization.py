# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-08 16:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TOFI', '0043_auto_20161208_0300'),
    ]

    operations = [
        migrations.CreateModel(
            name='Monetization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('describe_mon', models.CharField(max_length=100)),
                ('value_mon', models.FloatField()),
            ],
        ),
    ]
