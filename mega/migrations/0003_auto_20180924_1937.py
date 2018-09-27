# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-24 17:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mega', '0002_auto_20180924_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='centro',
            name='fecha_alta',
            field=models.DateField(default=datetime.datetime(2018, 9, 24, 17, 37, 9, 492437, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='fecha_alta',
            field=models.DateField(default=datetime.datetime(2018, 9, 24, 17, 37, 9, 493267, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='servicio',
            name='n_ir',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]