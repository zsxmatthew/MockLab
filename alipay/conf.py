import os

from django.conf import settings

sign_type = 'MD5'
notify_url = None
crypto_root = os.path.join(settings.BASE_DIR, 'alipay', '')
md5_secret = ''
is_success = 'T'
is_success_options = ['T', 'F']
trade_status_index = 2
