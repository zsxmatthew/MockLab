# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-27 08:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AlipayContext',
            fields=[
                ('out_trade_no', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('service', models.CharField(max_length=512)),
                ('context', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='AlipayUser',
            fields=[
                ('user_id', models.BigIntegerField(max_length=16, primary_key=True, serialize=False)),
            ],
        ),
    ]
