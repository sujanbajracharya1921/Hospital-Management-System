# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-02-16 13:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20190216_1921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Doctor'),
        ),
        migrations.AlterField(
            model_name='doctor_patient_med',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 2, 16, 13, 44, 38, 82703, tzinfo=utc), null=True),
        ),
    ]
