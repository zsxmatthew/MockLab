# --*-- coding: utf-8 --*--
import random
import string

import requests
from django.utils import timezone

from alipay_proxy import conf
from alipay_proxy.models import DutCustomerAgreementSign


def alipay_dut_customer_agreement_page_sign(context, agreement_id):
    url = context['notify_url']
    now = timezone.now()
    fmt = '%Y-%m-%d %H:%M:%S'
    notify_id = ''.join([random.choice(string.lowercase + string.digits) for _ in xrange(34)])
    agreement = DutCustomerAgreementSign.objects.get(pk=agreement_id)
    data = {
        'notify_time': now.strftime(fmt),
        'notify_type': 'dut_user_sign',
        'notify_id': notify_id,
        'sign_type': conf.sign_type,
        'agreement_no': agreement.agreement_no,
        'product_code': agreement.product_code,
        'scene': context.get('scene', 'DEFAULT|DEFAULT'),
        'status': agreement.status,
        'alipay_user_id': str(agreement.alipay_user_id),
        'sign_time': agreement.sign_time.strftime(fmt),
        'sign_modify_time': agreement.sign_modify_time.strftime(fmt),
        'valid_time': agreement.valid_time.strftime(fmt),
        'invalid_time': agreement.invalid_time.strftime(fmt),
        'partner_id': str(agreement.partner_id)
    }
    if 'external_sign_no' in context:
        data['external_sign_no'] = context['external_sign_no']
    text = "failed"
    while text != "success":
        resp = requests.post(url, data=data)
        print resp.text
        text = resp.text
