import os

from django.conf import settings

sign_type = 'MD5'
notify_url = 'https://newpay.etcp.cn/service/paymentnotify/notifyWithHolding'
crypto_root = os.path.join(settings.BASE_DIR, 'alipay', '')
md5_secret = ''
is_success = 'T'
trade_status_index = 2
