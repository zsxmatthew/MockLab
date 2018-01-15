# --*-- coding: utf-8 --*--
import copy
from threading import Thread

from alipay.models import AlipayUser
from alipay_proxy import notify
from utils.helpers import service2method, calc_delta
from alipay_proxy.models import DutCustomerAgreementSign


def alipay_dut_customer_agreement_page_sign(context):
    context_ = context.copy()
    # add a new Alipay user and a partner if necessary
    last_user = AlipayUser.objects.last()
    user_id = last_user and last_user.pk + 1 or 2088000000000000
    AlipayUser.objects.get_or_create(user_id=context_['partner'])
    AlipayUser.objects.create(user_id=user_id)
    # add a new Agreement Sign entry
    agreement = DutCustomerAgreementSign.objects.create(alipay_user_id=user_id,
                                                        partner_id=context_['partner'],
                                                        product_code=context_['product_code'],
                                                        external_sign_no=context_.get('external_sign_no', None))
    sign_time = agreement.sign_time
    # generate agreement_no
    fmt = "%Y%m%d%H%M%S"
    index = DutCustomerAgreementSign.objects.filter(
        agreement_no__startswith=sign_time.strftime(fmt)
    ).count() + 1
    agreement_no = '{}{}'.format(
        sign_time.strftime(fmt),
        str(index).zfill(6)
    )
    # calculate invalid_time
    validity_period = context_.get('sign_validity_period', '')
    delta = calc_delta(validity_period)
    DutCustomerAgreementSign.objects.filter(pk=agreement.pk).update(
        agreement_no=agreement_no,
        invalid_time=sign_time+delta
    )
    if "return_url" in context_:  # synchronized page redirection notification
        pass
    # post asynchronous notification
    client_method = service2method(context_.get('service', ''))
    if hasattr(notify, client_method) and 'notify_url' in context_:
        notify_thread = Thread(target=getattr(notify, client_method), args=(context_, agreement.pk))
        notify_thread.start()
    return context_
