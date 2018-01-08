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
