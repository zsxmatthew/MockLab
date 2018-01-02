# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from urlparse import parse_qsl, urlparse

from django.views.generic import TemplateView

from alipay_proxy import process
from ext.views.generic import JsonResponseMixin
from utils.helpers import service2method


class AlipayProxyView(JsonResponseMixin, TemplateView):
    def get_context_data(self, **kwargs):
        context_ = super(AlipayProxyView, self).get_context_data(**kwargs)
        context_.pop('view')  # view object should not be included in json response
        data = {}
        if self.request.method.upper() == 'GET':
            data.update(self.request.GET.dict())
        elif self.request.method.upper() == 'POST':
            data.update(self.request.POST.dict())
        # in case content type is not "x-www-form-urlencoded"
        if not data:
            try:
                data.update(json.loads(self.request.body))
            except ValueError:
                pass
        if 'scheme' in data:
            scheme = data['scheme']
        url = dict(parse_qsl(scheme)).get('url')
        if url:
            query = urlparse(url).query
            context_.update(dict(parse_qsl(query)))
        client_method = service2method(context_.get('service', ''))

        if hasattr(process, client_method):
            context = getattr(process, client_method)(context_)
        else:
            context = {}
        return context

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
