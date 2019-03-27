# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-03-26 14:40
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_auto_20190326_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='account.Doctor'),
        ),
        migrations.AlterField(
            model_name='doctor_patient_med',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 3, 26, 14, 40, 47, 167923, tzinfo=utc), null=True),
        ),
    ]