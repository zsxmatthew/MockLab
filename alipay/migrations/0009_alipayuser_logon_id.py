# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-01-15 02:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alipay', '0008_auto_20180112_1446'),
    ]

    operations = [
        migrations.AddField(
            model_name='alipayuser',
            name='logon_id',
            field=models.TextField(blank=True, null=True),
        ),
    ]
