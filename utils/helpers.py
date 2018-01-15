# --*-- coding: utf-8 --*--
import re
from urlparse import urlparse, urlunparse

from dateutil.relativedelta import relativedelta


def service2method(service):
    return '_'.join(service.split('.'))


def get_optional(data, old_name, new_name=None):
    """
    if old_name exists in data as a key, return a new dict using new_name as key
    and value of old_name in data as its value, or old_name as key if new_name is
    omitted
    :param data: source dict
    :param old_name: searching key in source dict
    :param new_name: optional, new key in source dict
    :return: new dict like {new_name: data[old_name]} or {old_name: data[old_name]}
    """
    if old_name in data:
        value = data.get(old_name)
        return {new_name or old_name: value}
    return {}


def calc_delta(desc):
    """
    translate period description to datetime delta
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


def proxy_parse(url, api, host='10.5.50.57', port='8000'):
    up = urlparse(url)
    return urlunparse([up[0], '{}:{}/proxy/{}'.format(host, port, api)] + list(up[2:]))


if __name__ == '__main__':
    url = "http://d.alipay.com/?scheme=alipays%3A%2F%2Fplatformapi%2Fstartapp%3" \
          "FappId%3D20000067%26url%3Dhttps%253A%252F%252Fmapi.alipay.com%252Fgateway.do" \
          "%253Fpartner%253D2088801473085644%2526_input_charset%253Dutf-8%2526service%" \
          "253Dalipay.dut.customer.agreement.page.sign%2526access_info%253D%" \
          "257B%2522channel%2522%253A%2522ALIPAYAPP%2522%257D%2526preAuth%253DYES%" \
          "2526notify_url%253Dhttp%253A%252F%252Fparking.qa.etcp.cn%252Fservice%" \
          "252Fwitholding%252Fnotify%2526product_code%253DGENERAL_WITHHOLDING_P%" \
          "2526external_sign_no%253Debc783b3-6141-42cd-b65c-04a5f1902aff%2526scene%" \
          "253DINDUSTRY%257CPARKING%2526sign_type%253DMD5%2526sign%253D389fdb266738ab21eaa5a4c4efc30ec5"
    print proxy_parse(url, 'sign')
