# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-17 22:24
from __future__ import unicode_literals

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('TOFI', '0011_auto_20161217_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rent',
            name='user_login',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
