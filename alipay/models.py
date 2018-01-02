# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class AlipayUser(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    pay_result = models.IntegerField(default=0)  # 0 means T


class AlipayContext(models.Model):
    trade_time = models.DateTimeField(auto_now_add=True)  # used to generate serials numbers
    trade_no = models.TextField(max_length=64, blank=True, null=True)
    partner = models.ForeignKey(AlipayUser)
    out_trade_no = models.CharField(max_length=64, primary_key=True)
    service = models.CharField(max_length=512)
    context = models.TextField(blank=True, null=True)




