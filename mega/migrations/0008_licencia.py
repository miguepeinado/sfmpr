# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-02-05 18:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mega', '0007_auto_20180929_1422'),
    ]

    operations = [
        migrations.CreateModel(
            name='Licencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=10)),
                ('numero', models.CharField(max_length=20)),
                ('servicio', models.ManyToManyField(to='mega.Servicio')),
            ],
        ),
    ]
