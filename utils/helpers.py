# --*-- coding: utf-8 --*--
import re

from dateutil.relativedelta import relativedelta


def service2method(service):
    return '_'.join(service.split('.'))


def get_optional(data, old_name, new_name=None):
    if old_name in data:
        value = data.get(old_name)
        return {new_name or old_name: value}
    return {}


def calc_delta(desc):
    """
    translate period description to delta
    :param desc: period description in <int><unit> format, unit could be m(=months), d(=days) and h(=hours), while 1c
    means ends of today
    :return: None if desc is '1c', otherwise delta object
    """
    m = re.match(r'(?P<months>\d+)m|(?P<days>\d+)d|(?P<hours>\d+)h|(?P<c>1c)', desc)
    if m:
        months, days, hours, c = m.group('months'), m.group('days'), m.group('hours'), m.group('c')
        if c:
            return None
        months = months and int(months) or 0
        days = days and int(days) or 0
        hours = hours and int(hours) or 0
        delta = relativedelta(days=days, months=months, hours=hours)
    else:
        delta = relativedelta(years=100)  # always valid
    return delta
