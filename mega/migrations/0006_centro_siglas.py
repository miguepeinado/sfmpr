# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-28 16:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mega', '0005_merge_20180928_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='centro',
            name='siglas',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
