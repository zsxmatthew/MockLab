# --*-- coding: utf-8 --*--
import random
import string

import requests
from django.utils import timezone

from alipay import conf
from alipay.sign import sign
from utils.helpers import get_optional


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
        'sign': sign(
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
