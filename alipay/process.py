# --*-- coding: utf-8 --*--
import json
import math
import random
import string
import urllib

import requests
from django.utils import timezone

from alipay import schema, conf, notify
from alipay.models import AlipayContext, AlipayUser
from utils.helpers import get_optional, service2method


def gen_trade_no(**kwargs):
    context = AlipayContext.objects.get(out_trade_no=kwargs['out_trade_no'])
    trade_no_prefix = context.trade_time.strftime('%Y%m%d')
    trade_no_prefix_long = context.trade_time.strftime('%Y%m%d%H%M%S')
    today_count = AlipayContext.objects.filter(trade_no__startswith=trade_no_prefix).count()
    trade_no = '{}{}'.format(
        trade_no_prefix_long,
        ('{:0>%d}' % (math.ceil(math.log10(today_count + 1)) <= 2 and 2 or 50)).format(today_count + 1)
    )
    AlipayContext.objects.filter(out_trade_no=kwargs['out_trade_no']).update(trade_no=trade_no)
    return trade_no


def wap_create_direct_pay_by_user(**kwargs):
    now = timezone.now()
    service = kwargs['service']
    context = {
        'notify_id': ''.join([random.choice(string.lowercase + string.digits) for _ in xrange(34)]),
        'notify_time': now.strftime('%Y-%m-%d %H:%M:%S'),
        'trade_no': gen_trade_no(**kwargs),
        'trade_status': schema.VOCABULARY[service][conf.trade_status_index]
    }
    for t in schema.RESP_SCHEMA.get(service):
        if not t[3]:  # mandatory
            if t[4][0] == 1:  # from conf
                context[t[0]] = getattr(conf, t[0])
            elif t[4][0] == 0 and len(t[4]) > 1:  # from request and has same name
                context[t[0]] = kwargs.get(t[4][1])
        else:  # optional
            if t[4][0] == 1:  # from conf
                context[t[0]] = getattr(conf, t[0])
            elif t[4][0] == 0 and len(t[4]) > 1:  # from request and has same name
                context.update(get_optional(kwargs, t[0], t[4][1]))
    context.update({
        'sign': ''  # not verified by merchant
    })
    if 'return_url' in kwargs:
        return_url = kwargs['return_url']
        host = "http://%(return_url)/alipay/return_url.php?%(data)" % {
            'return_url': return_url,
            'data': urllib.urlencode(context)
        }
        requests.get(host)  # TODO, not sure if here should be GET or POST
    return {}  # don't respond


def alipay_acquire_createandpay(**kwargs):
    AlipayContext.objects.create(out_trade_no=kwargs['out_trade_no'],
                                 service=kwargs['service'],
                                 partner_id=kwargs['partner'])
    now = timezone.now()
    trade_no = gen_trade_no(**kwargs)
    service = kwargs['service']
    _input_charset = kwargs.get('_input_charset')
    subject = kwargs.get('subject')
    buyer = None
    if 'buyer_id' in kwargs:
        buyer, buyer_created = AlipayUser.objects.get_or_create(user_id=kwargs['buyer_id'])
    if 'seller_id' in kwargs:
        AlipayUser.objects.get_or_create(user_id=kwargs['seller_id'])  # not really necessary
    context = {
        'is_success': conf.is_success_options[buyer.is_success] if buyer else conf.is_success,
        'subject': subject,
        'sign_type': conf.sign_type,
        'notify_url': kwargs.get('notify_url') or conf.notify_url,
        'trade_no': trade_no,
        'out_trade_no': kwargs.get('out_trade_no'),
        'result_code': 'ORDER_SUCCESS_PAY_SUCCESS',
        'total_fee': kwargs.get('total_fee'),
        'partner': kwargs.get('partner'),
        'gmt_payment': now.strftime('%Y-%m-%d %H:%M:%S'),
        '_input_charset': _input_charset,
        'product_code': kwargs.get('product_code'),
        'service': kwargs.get('service')
    }
    context.update(get_optional(kwargs, 'buyer_id'))
    context.update(get_optional(kwargs, 'buyer_id', 'buyer_user_id'))
    context.update(get_optional(kwargs, 'buyer_email'))
    context.update(get_optional(kwargs, 'buyer_email', 'buyer_logon_id'))
    context.update(get_optional(kwargs, 'seller_id'))
    context.update(get_optional(kwargs, 'body'))
    context.update(get_optional(kwargs, 'operator_id'))
    context.update(get_optional(kwargs, 'royalty_parameters'))
    context.update(get_optional(kwargs, 'royalty_type'))
    context.update(get_optional(kwargs, 'quantity'))
    context.update(get_optional(kwargs, 'dynamic_id_type'))
    context.update(get_optional(kwargs, 'alipay_ca_request'))
    context.update(get_optional(kwargs, 'price'))
    context.update(get_optional(kwargs, 'it_b_pay'))
    context.update(get_optional(kwargs, 'seller_email'))
    context.update(get_optional(kwargs, 'buyer_email'))
    context.update(get_optional(kwargs, 'operator_type'))
    context.update(get_optional(kwargs, 'show_url'))
    context.update(get_optional(kwargs, 'currency'))
    context.update(get_optional(kwargs, 'goods_detail'))
    context.update(get_optional(kwargs, 'extend_params'))
    context.update(get_optional(kwargs, 'channel_parameters'))
    context.update(get_optional(kwargs, 'ref_ids'))
    context.update(get_optional(kwargs, 'mcard_parameters'))
    context.update(get_optional(kwargs, 'auth_no'))
    context.update(get_optional(kwargs, 'promo_params'))
    context.update(get_optional(kwargs, 'passback_parameters'))
    context.update(get_optional(kwargs, 'agreement_info'))
    context['sign'] = ''  # fake one
    # context.update({
    #     'sign': sign(
    #         context,
    #         kwargs['_input_charset'],
    #         context.get('sign_type'),
    #         [item[0] for item in schema.RESP_SCHEMA.get(context['service'])],
    #         ['error', 'sign', 'sign_type', 'is_success']
    #     )
    # })

    # extract custom options
    options = json.loads(buyer.other_options) if buyer else {}
    if context['is_success'] == 'T':
        context.update(get_optional(options, 'detail_error_code'))
        context.update(get_optional(options, 'detail_error_des'))
        context.update(
            get_optional(options, 'result_code')
            or {'result_code': 'ORDER_SUCCESS_PAY_SUCCESS'})
        context.update(get_optional(options, 'extend_info'))
        context.update(get_optional(options, 'fund_bill_list'))
    if context['is_success'] == 'F' and options.get('error'):
        context['is_success'] = 'F'
        context['error'] = options.get('error')

    # callback parameters
    context.update(get_optional(kwargs, 'notify_action_type'))
    context.update(get_optional(kwargs, 'trade_status'))
    context.update(get_optional(kwargs, 'refund_fee'))
    context.update(get_optional(kwargs, 'out_biz_no'))
    context.update(get_optional(kwargs, 'paytools_pay_amount'))

    # assemble all parts of context
    _context = {
        'schema': get_schema(service),
        'context': context
    }

    # put complete context into context
    AlipayContext.objects.filter(out_trade_no=kwargs['out_trade_no']).update(context=json.dumps(_context))

    # asynchronous notification
    client_method = service2method(kwargs['service'])
    if hasattr(notify, client_method):
        getattr(notify, client_method)(context)
    return _context


def alipay_acquire_query(**kwargs):
    out_trade_no = kwargs.get('out_trade_no')
    context_ = json.loads(AlipayContext.objects.get(out_trade_no=out_trade_no).context)
    context = {}
    for t in schema.RESP_SCHEMA.get(kwargs.get('service')):
        if t[4][0] == 0:  # from request
            context[t[0]] = kwargs.get(t[0])
        elif t[4][0] == 1:  # from conf
            context[t[0]] = getattr(conf, t[0])
        elif t[4][0] == 3:  # from context
            if len(t[4]) > 1 and t[4][1] in context_['context']:
                context[t[0]] = context_['context'].get(t[4][1])
            elif t[0] in context_['context']:
                context[t[0]] = context_['context'].get(t[0])
    context['sign'] = ""  # TODO, client doesn't verify this

    context_['schema'] = get_schema(kwargs['service'])
    context_['context'].update(context)
    return context_


def get_schema(service):
    return {
        'req': {
            'mandatory': [field[0] for field in schema.REQ_SCHEMA[service] if not field[3]],
            'optional': [field[0] for field in schema.REQ_SCHEMA[service] if field[3]]
        },
        'resp': {
            'mandatory': [field[0] for field in schema.RESP_SCHEMA[service]
                          if not field[3] and field[0] not in ('sign', 'sign_type')],
            'optional': [field[0] for field in schema.RESP_SCHEMA[service]
                         if field[3] and field[0] not in ('sign', 'sign_type')]
        },
    }
