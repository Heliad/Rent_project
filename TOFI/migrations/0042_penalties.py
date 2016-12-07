# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-07 22:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TOFI', '0041_myuser_is_moder'),
    ]

    operations = [
        migrations.CreateModel(
            name='Penalties',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind_penalty', models.CharField(max_length=50)),
                ('describe_penalty', models.CharField(max_length=100)),
                ('cost_penalty', models.FloatField()),
            ],
        ),
    ]
