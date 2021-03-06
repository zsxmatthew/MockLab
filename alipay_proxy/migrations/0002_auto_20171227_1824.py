# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-27 10:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('alipay', '0001_initial'),
        ('alipay_proxy', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dutcustomeragreementsign',
            name='alipay_user_id',
        ),
        migrations.RemoveField(
            model_name='dutcustomeragreementsign',
            name='external_sign_no',
        ),
        migrations.AddField(
            model_name='dutcustomeragreementsign',
            name='alipay_user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_agreements', to='alipay.AlipayUser'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dutcustomeragreementsign',
            name='partner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='partner_agreements', to='alipay.AlipayUser'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dutcustomeragreementsign',
            name='product_code',
            field=models.CharField(default=django.utils.timezone.now, max_length=64),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dutcustomeragreementsign',
            name='agreement_no',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='dutcustomeragreementsign',
            name='invalid_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
