# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-12 15:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TOFI', '0047_auto_20161209_0233'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_rent', models.IntegerField()),
                ('image', models.ImageField(upload_to='images/')),
                ('name', models.CharField(max_length=100)),
                ('describe', models.CharField(max_length=150)),
            ],
        ),
    ]