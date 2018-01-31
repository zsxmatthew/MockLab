# --*-- coding: utf-8 --*--
import json

import requests
from django.utils import timezone
from simplejson import JSONDecodeError


class DefaultAlipayClient(object):
    def __init__(self, url, app_id, private_key, fmt,
                 charset, public_key, sign_type):
        self.url = url
        self.pub_request = dict(app_id=app_id,
                                format=fmt,
                                charset=charset,
                                sign_type=sign_type,
                                version="1.0")
        self.sign_type = sign_type
        self.private_key = private_key
        self.public_key = public_key

    def execute(self, request):
        biz_content = request.biz_content
        data = self.public_key.copy()
        data['method'] = request.method
        data['timestamp'] = timezone.now()
        data['biz_content'] = json.dumps(biz_content)
        data['sign'] = self.sign(data, self.sign_type, self.private_key, self.public_key)
        return DefaultAlipayResponse(requests.get(self.url, params=data))

    def sign(self, data, sign_type, private_key, public_key):
        return ''


class DefaultAlipayResponse(object):
    def __init__(self, response):
        self.response = response

    def __getattribute__(self, item):
        try:
            return object.__getattribute__(self, item)
        except AttributeError, e:
            if hasattr(self.response, item):
                return getattr(self.response, item)
            raise

    def is_success(self):
        try:
            return self.ok and self.json()['code'] == '10000'
        except (KeyError, JSONDecodeError):
            return False


class DefaultAlipayTradeRequest(object):
    def __init__(self):
        self.biz_content = {}
        self.method = None
        self.set_method()

    def set_biz_content(self, data=None, **kwargs):
        try:
            self.biz_content.update(json.loads(data))
        except TypeError:
            pass
        self.biz_content.update(kwargs)


class AlipayTradePayRequest(DefaultAlipayTradeRequest):
    def set_method(self):
        self.method = "alipay.trade.pay"


class AlipayTradeQueryRequest(DefaultAlipayTradeRequest):
    def set_method(self):
        self.method = "alipay.trade.query"
