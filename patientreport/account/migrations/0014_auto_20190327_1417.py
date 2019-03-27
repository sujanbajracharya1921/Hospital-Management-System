# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-03-27 08:32
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_auto_20190326_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='preffered_time',
            field=models.TimeField(default=None),
        ),
        migrations.AlterField(
            model_name='doctor_patient_med',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 3, 27, 8, 32, 27, 558637, tzinfo=utc), null=True),
        ),
    ]