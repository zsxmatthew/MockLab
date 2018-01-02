# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import random
import string

# Create your views here.
import requests

from Crypto.Random import random

from django.utils import timezone
from django.views.generic import TemplateView

from alipay import conf, process
from utils.helpers import service2method, get_optional


class AlipayView(TemplateView):
    template_name = 'alipay.xml'

    def get_context_data(self, **kwargs):
        context_ = super(AlipayView, self).get_context_data(**kwargs)
        context_.pop('view')
        if self.request.method.upper() == 'GET':
            context_.update(self.request.GET.dict())
        elif self.request.method.upper() == 'POST':
            context_.update(self.request.POST.dict())
        # in case content type is not "x-www-form-urlencoded"
        if not context_:
            try:
                context_.update(json.loads(self.request.body))
            except ValueError:
                pass

        client_method = service2method(context_.get('service', ''))

        if hasattr(process, client_method):
            return getattr(process, client_method)(**context_)
        else:
            return {}

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


def asynch_notify(context, encoding=None, key_spec=[]):
    now = timezone.now()
    notify_id = ''.join([random.choice(string.lowercase + string.digits) for _ in xrange(34)])
    data = {
        'notify_time': now.strftime('%Y-%m-%d %H:%M:%S'),
        'notify_type': 'trade_status_sync',
        'notify_id': notify_id,
        'sign_type': conf.sign_type,
        'notify_action_type': context.get('notify_action_type') or 'payByAccountAction',
        'out_trade_no': context.get('out_trade_no'),
        'subject': context.get('subject'),
        'trade_no': context.get('trade_no'),
        'trade_status': context.get('trade_status') or 'TRADE_SUCCESS',
        'gmt_create': context.get('gmt_payment'),  # don't know where this is from
        'gmt_payment': context.get('gmt_payment'),
        'total_fee': context.get('total_fee')
    }
    data.update(get_optional(context, 'seller_email'))
    data.update(get_optional(context, 'buyer_email'))
    data.update(get_optional(context, 'seller_id'))
    data.update(get_optional(context, 'buyer_id'))
    data.update(get_optional(context, 'price'))
    data.update(get_optional(context, 'quantity'))
    data.update(get_optional(context, 'buyer_email'))
    data.update(get_optional(context, 'body'))
    data.update(get_optional(context, 'refund_fee'))
    data.update(get_optional(context, 'out_biz_no'))
    data.update(get_optional(context, 'paytools_pay_amount'))
    data.update(get_optional(context, 'passback_parameters', 'extra_common_param'))
    data.update({
        'sign': process.sign(
            data,
            encoding,
            context.get('sign_type'),
            key_spec)
    })
    resp = requests.post(context.get('notify_url'), data=data)
    print 'asynch_notify_params'.center(40, '-')
    for k, v in data.items():
        print k, ':', v
    print 'asynch_notify_resp'.center(40, '-')
    print resp.status_code
    print resp.headers['content-type']
    print resp.encoding
    print resp.text
