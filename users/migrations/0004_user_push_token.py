# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-22 21:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20170812_2337'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='push_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
