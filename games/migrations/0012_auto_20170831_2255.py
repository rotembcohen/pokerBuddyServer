# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-31 22:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0011_bet_is_confirmed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bet',
            name='is_confirmed',
        ),
        migrations.AddField(
            model_name='payment',
            name='is_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
