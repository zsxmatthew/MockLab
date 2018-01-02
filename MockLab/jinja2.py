# --*-- utf-8 --*--
from __future__ import absolute_import  # Python 2 only

from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse

from jinja2 import Environment
from django.utils.translation import ugettext, ungettext


def environment(**options):
    env = Environment(**options)
    env.install_gettext_callables(ugettext, ungettext, newstyle=True)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env
