# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-11 21:21
from __future__ import unicode_literals

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_app_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='chip_basic_unit',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
    ]
