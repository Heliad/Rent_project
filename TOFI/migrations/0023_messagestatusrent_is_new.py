# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-27 22:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TOFI', '0022_messagestatusrent_login_user_from'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagestatusrent',
            name='is_new',
            field=models.BooleanField(default=True),
        ),
    ]
