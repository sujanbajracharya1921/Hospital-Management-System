# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-02-16 13:36
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20190216_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='department',
            field=models.CharField(choices=[('OPD', 'OPD'), ('Operation', 'Operation'), ('ENT', 'ENT'), ('Skin', 'Skin'), ('Eye', 'Eye'), ('Heart', 'Heart')], default='OPD', max_length=50),
        ),
        migrations.AlterField(
            model_name='doctor_patient_med',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2019, 2, 16, 13, 36, 3, 765518, tzinfo=utc), null=True),
        ),
    ]