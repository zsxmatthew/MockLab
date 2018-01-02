# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from alipay.models import AlipayUser


class DutCustomerAgreementSign(models.Model):
    agreement_no = models.CharField(max_length=20, unique=True,
                                    blank=True, null=True)
    alipay_user = models.ForeignKey(AlipayUser, related_name='user_agreements')
    sign_time = models.DateTimeField(auto_now_add=True)
    sign_modify_time = models.DateTimeField(auto_now=True)
    valid_time = models.DateTimeField(auto_now_add=True)
    invalid_time = models.DateTimeField(blank=True, null=True)
    product_code = models.CharField(max_length=64)
    partner = models.ForeignKey(AlipayUser, related_name='partner_agreements')
    status = models.CharField(choices=(('TEMP', 'TEMP'),
                                       ('NORMAL', 'NORMAL'),
                                       ('STOP', 'STOP')),
                              default='NORMAL', max_length=6)
