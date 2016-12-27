# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-26 23:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('TOFI', '0029_auto_20161226_2223'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_pic', models.ImageField(default='pic_folder/None/no-img.jpg', upload_to='pic_folder/')),
                ('name', models.CharField(max_length=50)),
                ('describe', models.CharField(max_length=150)),
            ],
        ),
        migrations.AddField(
            model_name='rent',
            name='images',
            field=models.ManyToManyField(default=0, to='TOFI.ImageModel'),
        ),
    ]
