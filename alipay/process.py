# --*-- coding: utf-8 --*--
import json
import math
import random
import string
import urllib
from threading import Thread

import requests
import time
from django.http import Http404
from django.utils import timezone

from alipay import schema, conf, notify
from alipay.models import AlipayContext, AlipayUser
from alipay_proxy.models import DutCustomerAgreementSign
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


def wap_create_direct_pay_by_user(view, **kwargs):
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


def alipay_acquire_createandpay(view, **kwargs):
    view.template_name = 'alipay_acquire_createandpay.xml'
    service = kwargs['service']
    AlipayContext.objects.create(out_trade_no=kwargs['out_trade_no'],
                                 service=service,
                                 partner_id=kwargs['partner'])
    now = timezone.now()
    trade_no = gen_trade_no(**kwargs)
    buyer = None
    if 'buyer_id' in kwargs:
        buyer, buyer_created = AlipayUser.objects.get_or_create(user_id=kwargs['buyer_id'])
    if 'seller_id' in kwargs:
        AlipayUser.objects.get_or_create(user_id=kwargs['seller_id'])  # not really necessary
    context = {
        'is_success': conf.is_success_options[buyer.is_success] if buyer else conf.is_success,
        'sign_type': conf.sign_type,
        'trade_no': trade_no,
        'out_trade_no': kwargs.get('out_trade_no'),
        'total_fee': kwargs.get('total_fee'),
        'gmt_payment': now.strftime('%Y-%m-%d %H:%M:%S')
    }
    context.update(get_optional(kwargs, 'buyer_id', 'buyer_user_id'))
    context.update(get_optional(kwargs, 'buyer_email', 'buyer_logon_id'))
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
    options = json.loads(buyer.other_options or '{}').get(service, {}) if buyer else {}
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

    # callback parameters including all fields from request and response
    callback = {}
    callback.update(kwargs)
    callback.update(context)

    # assemble all parts of context
    context_ = {
        'request_': kwargs,  # using 'request' here would shadow another argument in deeper methods
        'schema': get_schema(service),
        'response': context,
        'callback': callback
    }

    # put complete context into context
    AlipayContext.objects.filter(out_trade_no=kwargs['out_trade_no']).update(
        context=json.dumps(context_),
        trade_no=trade_no
    )

    # asynchronous notification
    client_method = service2method(kwargs['service'])
    if hasattr(notify, client_method):
        getattr(notify, client_method)(context)

    Thread(target=trigger_query).start()

    return context_


def alipay_acquire_query(view, **kwargs):
    out_trade_no = kwargs.get('out_trade_no')
    try:
        trade_context = json.loads(AlipayContext.objects.get(out_trade_no=out_trade_no).context)
    except AlipayContext.DoesNotExist:
        raise Http404('Trade does not exist.')
    context = {}
    for t in schema.RESP_SCHEMA.get(kwargs.get('service')):
        if t[4][0] == 0:  # from request
            context[t[0]] = kwargs.get(t[0])
        elif t[4][0] == 1:  # from conf
            context[t[0]] = getattr(conf, t[0])
        elif t[4][0] == 3:  # from context
            if len(t[4]) > 1 and t[4][1] in trade_context['response']:
                context[t[0]] = trade_context['response'].get(t[4][1])
            elif t[0] in trade_context['context']:
                context[t[0]] = trade_context['response'].get(t[0])
    context['sign'] = ""  # TODO, client doesn't verify this

    context_ = {
        'request_': kwargs,
        'schema': get_schema(kwargs['service']),
        'response': context
    }
    return context_


def alipay_dut_customer_agreement_query(view, **kwargs):
    view.template_name = 'alipay_dut_customer_agreement_query.xml'
    user = None
    try:
        if 'alipay_user_id' in kwargs:
            agreements = DutCustomerAgreementSign.objects.filter(partner_id=kwargs['partner'],
                                                                 alipay_user_id=kwargs['alipay_user_id'])
        else:
            agreements = DutCustomerAgreementSign.objects.filter(partner_id=kwargs['partner'],
                                                                 alipay_user__logon_id=kwargs['alipay_logon_id'])
        if 'external_sign_no' in kwargs:
            agreement = agreements.get(external_sign_no=kwargs['external_sign_no'])
        else:
            agreement = agreements.first()
        status = agreement.status
        valid_time = agreement.valid_time.strftime('%Y-%m-%d %H:%M:%S')
        invalid_time = agreement.invalid_time.strftime('%Y-%m-%d %H:%M:%S')
        sign_time = agreement.sign_time.strftime('%Y-%m-%d %H:%M:%S')
        sign_modify_time = agreement.sign_modify_time.strftime('%Y-%m-%d %H:%M:%S')
        external_sign_no = agreement.external_sign_no or None
        agreement_detail = agreement.agreement_detail or None
        agreement_no = agreement.agreement_no or None
    except DutCustomerAgreementSign.DoesNotExist:
        # status = 'STOP'
        # valid_time = '1970-01-01 00:00:01'
        # invalid_time = '1970-01-01 00:00:01'
        # sign_time = '1970-01-01 00:00:01'
        # sign_modify_time = '1970-01-01 00:00:01'
        # external_sign_no = None
        # agreement_detail = None
        raise Http404('No result found.')
    if 'alipay_user_id' in kwargs:
        try:
            user = AlipayUser.objects.get(user_id=kwargs['alipay_user_id'])
        except AlipayUser.DoesNotExist:
            user = None
    context = {
        'is_success': conf.is_success_options[user.is_success] if user else 'F',
        'sign_type': 'MD5',  # optional
        'sign': '',  # TODO, fake and optional
        'pricipal_type': 'CARD' if 'alipay_user_id' in kwargs else 'CUSTOMER',
        'principal_id': kwargs.get('alipay_user_id') or kwargs.get('alipay_logon_id'),
        'product_code': kwargs['product_code'],
        'scene': kwargs['scene'] or 'DEFAULT|DEFAULT',
        'thirdpart_type': 'PARTNER',
        'thirdpart_id': kwargs['partner'],
        'status': status,
        'valid_time': valid_time,
        'invalid_time': invalid_time,
        'sign_time': sign_time,
        'sign_modify_time': sign_modify_time,
        'agreement_detail': agreement_detail or '{}',
        'agreement_no': agreement_no
    }
    if external_sign_no:  # optional
        context['external_sign_no'] = external_sign_no
    if context['is_success'] == 'F':  # error should not be available if query succeeds
        context.update(get_optional(kwargs, 'error'))
    context_ = {
        'request_': kwargs,
        'schema': get_schema(kwargs['service']),
        'response': context
    }
    return context_


def alipay_trade_pay(view, **kwargs):  # bar code, json response
    view.format = 'json'
    biz_content = json.loads(kwargs['biz_content'])
    service = kwargs['method']
    try:
        partner = AlipayUser.objects.get(app_id=kwargs['app_id'])
    except AlipayUser.DoesNotExist:
        raise Http404('Invalid app_id that does not match with any partner.')
    AlipayContext.objects.create(out_trade_no=biz_content['out_trade_no'],
                                 service=service,
                                 partner=partner)
    now = timezone.now()
    trade_no = gen_trade_no(**biz_content)
    if 'buyer_id' in biz_content:
        buyer, buyer_created = AlipayUser.objects.get_or_create(user_id=biz_content['buyer_id'])
    else:
        last_user = AlipayUser.objects.last()
        user_id = last_user and last_user.pk + 1 or 2088000000000000
        buyer = AlipayUser.objects.create(user_id=user_id)
    options = json.loads(buyer.other_options or '{}').get(service, {})
    code = options.get('code', None) or '10000'
    sub_code = options.get('sub_code', None)
    context = {
        # public
        'code': code,
        'msg': schema.VOCABULARY[kwargs['method']]['code'][code],
        'sign': '',  # TODO, fake
        # business
        'trade_no': trade_no,
        'out_trade_no': biz_content['out_trade_no'],
        'buyer_logon_id': buyer.logon_id or '',
        'total_amount': biz_content['total_amount'],
        'receipt_amount': biz_content['total_amount'],  # TODO
        'gmt_payment': now.strftime('%Y-%m-%d %H:%M:%S'),
        'fund_bill_list': json.dumps({
            "fund_channel": options.get('fund_channel') or 'ALIPAYACCOUNT',
            "amount": biz_content['total_amount']  # TODO
        }),
        'buyer_user_id': buyer.user_id
    }
    if sub_code:
        context['sub_code'] = sub_code
        category = 'public' if code != '40004' else kwargs['method']
        try:
            context['sub_msg'] = schema.VOCABULARY[category]['sub_code'][sub_code][0]
        except KeyError:
            raise Http404('Improper configuration for current buyer: category of sub_code '
                          'is not in coincidence with code')
    context.update(get_optional(options, 'buyer_pay_amount'))
    context.update(get_optional(options, 'point_amount'))
    context.update(get_optional(options, 'invoice_amount'))
    context.update(get_optional(options, 'card_balance'))
    context.update(get_optional(options, 'store_name'))
    context.update(get_optional(options, 'discount_goods_detail'))
    context.update(get_optional(options, 'voucher_detail_list'))
    context.update(get_optional(options, 'business_params'))
    context.update(get_optional(options, 'buyer_user_type'))

    # assemble all parts of context
    context_ = {
        'request_': kwargs,
        'scheme': get_schema(kwargs['method']),
        'response': context
    }

    # put complete context into context
    AlipayContext.objects.filter(out_trade_no=biz_content['out_trade_no']).update(
        context=json.dumps(context_),
        trade_no=trade_no
    )

    return context


def alipay_trade_query(view, **kwargs):
    view.format = 'json'
    try:
        biz_content = json.loads(kwargs['biz_content'])
        if 'trade_no' in biz_content:
            trade = AlipayContext.objects.get(trade_no=biz_content['trade_no'])
        else:
            trade = AlipayContext.objects.get(out_trade_no=biz_content['out_trade_no'])
        trade_context = json.loads(trade.context)
    except AlipayContext.DoesNotExist:
        raise Http404('Trade does not exist.')
    context = {
        # public
        'code': '1000',  # TODO, generally speaking we don't make such query directly in testing
        'msg': schema.VOCABULARY['public']['1000'],
        'sign': '',  # TODO, fake
        # business
        'trade_no': trade_context['response']['trade_no'],
        'out_trade_no': trade_context['response']['out_trade_no'],
        'buyer_logon_id': trade_context['response']['buyer_logon_id'],
        'trade_status': 'TRADE_SUCCESS' if trade_context['response']['code'] == '10000' else 'TRADE_CLOSED',
        'total_amount': trade_context['response']['total_amount'],
        'fund_bill_list': trade_context['response']['fund_bill_list'],
        'buyer_user_id': trade_context['response']['buyer_user_id'],
    }
    context.update(get_optional(trade_context['response'], 'receipt_amount'))
    context.update(get_optional(trade_context['response'], 'buyer_pay_amount'))
    context.update(get_optional(trade_context['response'], 'point_amount'))
    context.update(get_optional(trade_context['response'], 'invoice_amount'))
    context.update(get_optional(trade_context['request'], 'store_id'))
    context.update(get_optional(trade_context['request'], 'terminal_id'))
    context.update(get_optional(trade_context['response'], 'store_name'))
    context.update(get_optional(trade_context['response'], 'buyer_user_type'))

    return context


def mobile_securitypay_pay(view, **kwargs):  # mobile app pay
    """
    partner="2088801473085644"&seller_id="zhifubao@etcp.cn"&out_trade_no="p1516695671513110859803"
    &subject="ETCP停车费支付"&body="ETCP停车费支付"&total_fee="0.01"
    &notify_url="http://newpay.test.etcp.cn/service/paymentnotify/notifyalipay"&service="mobile.securitypay.pay"
    &payment_type="1"&_input_charset="utf-8"&it_b_pay="30m"&extend_params={"AGENT_ID":"2088821587787865"}
    &return_url="m.alipay.com"
    :param kwargs:
    :return:
    """
    buyer, buyer_created = AlipayUser.objects.get_or_create(user_id=kwargs.get('partner'))
    result_status = None
    orig = u'&'.join(['{}="{}"'.format(k, v) for k, v in kwargs.items() if k not in ('sign_type', 'sign')])
    option = json.loads(buyer.other_options or '{}').get(kwargs['service'], {})
    success = option.get('success', 'true')
    result = orig + 'success="{}"'


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


def trigger_query():
    time.sleep(3)
    requests.get(conf.trade_center_host + '/service/trade/2.2.2/queryOrderByAllWithhold')
