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
from ext.views.generic import JsonResponseMixin
from utils.helpers import service2method, get_optional


class AlipayView(JsonResponseMixin, TemplateView):
    template_name = 'alipay.xml'

    def __init__(self, **kwargs):
        super(AlipayView, self).__init__(**kwargs)
        self.format = 'xml'  # identify mapi or openapi

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

        if 'service' in context_:
            client_method = service2method(context_.get('service', ''))  # mapi
        elif 'method' in context_:
            client_method = service2method(context_.get('method', ''))  # openapi
        else:
            client_method = ''

        if 'format' in context_:  # this field only exists in public part of openapi request
            self.format = context_['format'].lower()

        if hasattr(process, client_method):
            return getattr(process, client_method)(**context_)
        else:
            return {}

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        if self.format == 'json':  # openapi only supports json response
            return self.render_to_json_response(context, **response_kwargs)
        else:  # mapi supports xml so far
            return super(AlipayView, self).render_to_response(context, **response_kwargs)
