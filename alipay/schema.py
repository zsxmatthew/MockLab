# -*- coding: utf-8 -*-
# field_name, field_type, field_restrictions, nullable, source_type, description
# source_type:
#   0 - from request
#   1 - from conf
#   2 - generated
#   3 - from context
#   4 - from request optional, with default value
#   5 - default value

REQ_SCHEMA = {
    'alipay.acquire.createandpay': (
        ('service', 'string', (), False, u'接口名称'),
        ('partner', 'string', (16, ), False, u'合作者身份ID'),  # r'2088\d{12}'
        ('_input_charset', 'string', (), False, u'参数编码字符集'),  # utf-8, gbk, gb2312
        ('sign_type', 'string', (), False, u'签名方式'),  # DSA, RSA, MD5
        ('sign', 'string', (), False, u'签名'),
        ('notify_url', 'string', (190, ), True, u'服务器异步通知页面路径'),
        ('alipay_ca_request', 'string', (), True, u'签名类型'),  # 1: certificates, 2: other secret keys, 2 when omitted
        ('out_trade_no', 'string', (64, ), False, u'商户网站唯一订单号'),
        ('subject', 'string', (256, ), False, u'订单标题'),  # at most 128 Chinese characters
        # BARCODE_PAY_OFFLINE
        # SOUNDWAVE_PAY_OFFLINE
        # MEMBER_CARD_QR_OFFLINE
        # FUND_TRADE_FAST_PAY
        # FINGERPRINT_FAST_PAY
        ('product_code', 'string', (32, ), False, u'订单业务类型'),
        ('total_fee', 'number', (9, 2), False, u'订单金额'),
        ('seller_id', 'string', (28, ), True, u'卖家支付宝用户号'),
        ('seller_email', 'string', (100, ), True, u'卖家支付宝账号'),
        ('buyer_id', 'string', (28, ), True, u'买家支付宝用户号'),  # 16 digits starting with 2088
        ('buyer_email', 'string', (100, ), True, u'买家支付宝账号'),
        # 0: alipay operators, 1: merchant operators, 1 when omitted
        ('operator_type', 'string', (1, ), True, u'操作员类型'),
        ('operator_id', 'string', (28, ), True, u'操作员号'),
        ('body', 'string', (400, ), True, u'订单描述'),
        ('show_url', 'string', (400, ), True, u'商品展示网址'),
        ('currency', 'string', (10, ), True, u'订单金额币种'),  # 156 only
        ('price', 'number', (9, 2), True, u'商品单价'),  # total_fee = price * quantity
        ('quantity', 'string', (100, ), True, u'商品数量'),  # total_fee = price * quantity
        ('goods_detail', 'json', (), True, u'商品明细'),
        ('extend_params', 'json', (128, ), True, u'公用业务扩展信息'),
        ('it_b_pay', 'string', (200, ), True, u'订单支付超时时间'),  # 1m ~ 15d
        ('royalty_type', 'string', (150, ), True, u'分账类型'),  # ROYALTY only
        ('royalty_parameters', 'json', (2000, ), True, u'分账信息'),
        ('channel_parameters', 'json', (256, ), True, u'渠道参数'),
        ('dynamic_id_type', 'string', (32, ), True, u'动态ID类型'),  # wave_code, bar_code, must be provided if dynamic_id is available
        ('dynamic_id', 'string', (32, ), True, u'动态ID'),  # either buyer_id or dynamic_id must be provided
        ('ref_ids', 'json', (256, ), True, u'关联ID集合'),
        ('mcard_parameters', 'json', (256, ), True, u'预付卡相关参数'),
        ('auth_no', 'string', (32, ), True, u'授权号'),  # must be provided if product_code is FUND_TRADE_FAST_PAY, otherwise must be omitted
        ('promo_params', 'json', (256, ), True, u'优惠参数'),
        ('passback_parameters', 'string', (256, ), True, u'业务透传参数'),
        ('agreement_info', 'json', (256, ), True, u'协议信息')
    ),
    'alipay.wap.create.direct.pay.by.user': (
        ('service', 'string', (), False, u'接口名称'),
        ('partner', 'string', (16,), False, u'合作者身份ID'),  # r'2088\d{12}'
        ('_input_charset', 'string', (), False, u'参数编码字符集'),  # utf-8, gbk, gb2312
        ('sign_type', 'string', (), False, u'签名方式'),  # DSA, RSA, MD5
        ('sign', 'string', (), False, u'签名'),
        ('notify_url', 'string', (190,), True, u'服务器异步通知页面路径'),
        ('return_url', 'string', (200,), True, u'页面跳转同步通知页面路径'),
        ('out_trade_no', 'string', (64,), False, u'商户网站唯一订单号'),
        ('subject', 'string', (256,), False, u'订单标题'),  # at most 128 Chinese characters
        ('total_fee', 'number', (9, 2), False, u'订单金额'),
        ('seller_id', 'string', (28,), True, u'卖家支付宝用户号'),
        ('payment_type', 'string', (4,), False, u'支付类型'),
        ('body', 'string', (1000,), True, u'商品描述'),
        ('show_url', 'string', (400,), True, u'商品展示网址'),
        ('it_b_pay', 'string', (200,), True, u'订单支付超时时间'),  # 1m ~ 15d
        ('extern_token', 'string', (), True, u'钱包token'),
        ('otherfee', 'number', (9, 2), True, u'航旅订单其它费用'),
        ('airticket', 'string', (1, 64), True, u'航旅订单金额')  # r'(\d+\^\w+(|\d+\^\w+)*)?'
    ),
    'alipay.acquire.query': (
        ('service', 'string', (), False, u'接口名称'),
        ('partner', 'string', (16,), False, u'合作者身份ID'),  # r'2088\d{12}'
        ('_input_charset', 'string', (), False, u'参数编码字符集'),  # utf-8, gbk, gb2312
        ('sign_type', 'string', (), False, u'签名方式'),  # DSA, RSA, MD5
        ('sign', 'string', (), False, u'签名'),
        # 1: cert
        # 2: other secret keys
        ('alipay_ca_request', (), True, u'签名类型'),  # default 2
        ('out_trade_no', 'string', (64,), False, u'商户网站唯一订单号'),
        ('trade_no', 'string', (64,), True, u'支付宝交易号')
    ),
    'alipay.dut.customer.agreement.page.sign': (
        ('service', 'string', (), False, u'接口名称'),
        ('partner', 'string', (16,), False, u'合作者身份ID'),  # r'2088\d{12}'
        ('sign_type', 'string', (), False, u'签名方式'),
        ('sign', 'string', (), False, (2,), u'签名'),
        ('_input_charset', 'string', (), True, u'参数编码字符集'),
        ('return_url', 'string', (200,), True, u'页面跳转同步通知页面路径'),
        ('notify_url', 'string', (200,), True, u'服务器异步通知页面路径'),
        ('proudct_code', 'string', (64,), False, u'产品码'),
        ('access_info', 'json', (), False, u'接入信息'),
        ('scene', 'string', (64,), True, u'签约场景'),  # default to DEFAULT|DEFAULT
        # currently supports:
        # d: day
        # m: month
        # eg. 2m
        ('sign_validity_period', 'string', (8,), True, u'签约有效期'),
        ('external_sign_no', 'string', (32,), True, u'商户签约号'),
        ('agreement_detail', 'json', (), True, u'协议细则'),
        ('prod_properties', 'json', (), True, u'签约产品属性'),
        ('external_user_id', 'string', (), True, u'商户网站用户标识')
    )
}

RESP_SCHEMA = {
    'alipay.acquire.createandpay': (
        # ('is_success', 'string', (), False, u'请求是否成功'),  # T, F
        ('sign_type', 'string', (), True, u'签名方式'),  # DSA, RSA, MD5
        ('sign', 'string', (), True, u'签名'),
        ('error', 'string', (), True, u'错误代码'),
        ('result_code', 'string', (32, ), False, u'响应码'),
        ('trade_no', 'string', (64, ), True, u'支付宝交易号'),
        ('out_trade_no', 'string', (64, ), True, u'商户网站唯一订单号'),
        ('buyer_user_id', 'string', (30, ), True, u'买家支付宝用户号'),  # 16 digits starting with 2088
        ('buyer_logon_id', 'string', (100, ), True, u'买家支付宝账号'),
        ('total_fee', 'number', (), True, u'交易金额'),  # same to the total_fee in request
        ('gmt_payment', 'date', (), True, u'交易付款时间'),  # yyyy-MM-dd HH:mm:ss
        ('detail_error_code', 'string', (48, ), True, u'详细错误码'),  # omitted when result_code is ORDER_SUCCESS_PAY_SUCCESS
        ('detail_error_des', 'string', (64, ), True, u'详细错误描述'),  # omitted when result_code is ORDER_SUCCESS_PAY_SUCCESS
        ('extend_info', 'json', (256, ), True, u'返回扩展信息'),
        ('fund_bill_list', 'xml', (), True, u'本次交易支付单据信息集合'),
    ),
    'alipay.wap.create.direct.pay.by.user': (
        ('is_success', 'string', (1,), False, (1,), u'成功标识'),
        ('sign_type', 'string', (), False, (1,), u'签名方式'),  # DSA, RSA, MD5
        ('sign', 'string', (32,), False, (2,), u'签名'),
        ('service', 'string', (), True, (0,), u'接口名称'),
        ('notify_id', 'string', (), True, (2,), u'通知校验ID'),
        ('notify_time', 'date', (), True, (2,), u'通知时间'),  # yyyy-MM-dd HH:mm:ss
        ('out_trade_no', 'string', (64,), (0,), True, u'商户网站唯一订单号'),
        ('trade_no', 'string', (64,),True, (2,), u'支付宝交易号'),
        ('subject', 'string', (256,), True, (0,), u'商品名称'),
        ('payment_type', 'string', (4,), True, (0,), u'支付类型'),
        ('trade_status', 'string', (), True, (2,), u'交易状态'),
        ('seller_id', 'string', (30,), True, (0,), u'卖家支付宝账户号'),
        ('total_fee', 'number', (9, 2), True, (0,), u'交易金额'),
        ('body', 'string', (400,), True, (0,), u'商品描述')
    ),
    'alipay.acquire.query': (
        # ('is_success', 'string', (1,), False, (3,), u'请求是否成功'),
        ('sign_type', 'string', (), True, (1,), u'签名方式'),  # DSA, RSA, MD5
        ('sign', 'string', (32,), True, (2,), u'签名'),
        ('error', 'string', (), True, (3,), u'接口名称'),
        ('result_code', 'string', (32,), False, (3,), u'响应码'),
        ('trade_no', 'string', (64,), True, (3,), u'支付宝交易号'),
        ('out_trade_no', 'string', (64,), True, (0,), u'商户网站唯一订单号'),
        ('buyer_user_id', 'string', (16,), True, (3,), u'买家支付宝用户号'),
        ('buyer_logon_id', 'string', (100,), True, (3,), u'买家支付宝账号'),
        ('partner', 'string', (100,), True, (3,), u'合作者身份ID'),
        ('trade_status', 'string', (32,), True, (3,), u'交易状态'),
        ('detail_error_code', 'string', (48,), True, (3,), u'详细错误码'),
        ('detail_error_des', 'string', (64,), True, (3,), u'详细错误描述'),
        ('fund_bill_list', 'xml', (), True, (3,), u'本次交易支付单据信息集合'),
        ('total_fee', 'string', (), True, (3,), u'订单金额'),
        ('send_pay_date', 'string', (), True, (3,), u'本次交易打款给卖家的时间'),  # yyyy-MM-dd HH:mm:ss
        ('extend_info_list', 'xml', (), True, (3,), u'本次交易返回的扩展信息')
    ),
    'alipay.dut.customer.agreement.page.sign': (
        ('is_success', 'string', (1,), False, (1,), u'是否成功'),
        ('sign_type', 'string', (), False, (1,), u'签名方式'),  # DSA, RSA, MD5
        ('sign', 'string', (32,), False, (2,), u'签名'),
        ('_input_charset', 'string', (), True, (1,), u'参数编码字符集'),
        ('agreement_no', 'string', (), False, (2,), u'协议号'),
        ('product_code', 'string', (), False, (0,), u'产品码'),
        ('scene', 'string', (), False, (4, 'DEFAULT|DEFAULT'), u'签约场景'),
        # TEMP: never been effective
        # NORMAL
        # STOP
        ('status', 'string', (), False, (1,), u'协议状态'),
        ('sign_time', 'date', (), False, (2,), u'签约时间'),  # yyyy-MM-dd HH:mm:ss
        ('sign_modify_time', 'date', (), False, (2,), u'签约修改时间'),  # same to sign_time if never changed
        ('valid_time', 'date', (), False, (2,), u'协议生效时间'),  # yyyy-MM-dd HH:mm:ss
        ('invalid_time', 'date', (), False, (2,), u'协议失效时间'),  # yyyy-MM-dd HH:mm:ss
        ('alipay_user_id', 'string', (16), False, (2,), u'支付宝用户号'),  # r'2088\d{12}'
        ('external_sign_no', 'string', (), True, (0,), u'商户签约号')
    )
}

ASYNCH_NOTIFY_SCHEMA = {
    'alipay.acquire.createandpay': (
        ('notify_time', 'date', (), False, u'通知时间'),  # yyyy-MM-dd HH:mm:ss
        ('notify_type', 'string', (), False, u'通知类型'),
        ('notify_id', 'string', (), False, u'通知校验ID'),
        ('sign_type', 'string', (), False, u'签名方式'),  # DSA, RSA, MD5
        ('sign', 'string', (32,), False, u'签名'),
        # createDirectPayTradeByBuyerAction
        # payByAccountAction
        # refundFPAction
        # reverseAction
        # closeTradeAction
        # finishFPAction
        ('notify_action_type', 'string', (), True, u'通知动作类型'),
        ('out_trade_no', 'string', (64,), True, u'商户网站唯一订单号'),
        ('subject', 'string', (256,), True, u'商品名称'),
        ('trade_no', 'string', (64,), True, u'支付宝交易号'),
        ('trade_status', 'string', (), True, u'交易状态'),
        ('gmt_create', 'date', (), True, u'交易创建时间'),  # yyyy-MM-dd HH:mm:ss
        ('gmt_payment', 'date', (), True, u'交易付款时间'),  # yyyy-MM-dd HH:mm:ss
        ('seller_email', 'string', (100,), True, u'卖家支付宝账号'),  # email or mobile
        ('buyer_email', 'string', (100,), True, u'买家支付宝账号'),  # email or mobile
        ('seller_id', 'string', (30,), True, u'卖家支付宝账户号'),  # r'2088\d{12}'
        ('buyer_id', 'string', (30,), True, u'买家支付宝账户号'),  # r'2088\d{12}'
        ('price', 'number', (), True, u'商品单价'),
        ('quantity', 'number', (), True, u'购买数量'),
        ('total_fee', 'number', (), True, u'交易金额'),
        ('body', 'string', (400,), True, u'商品描述'),
        ('refund_fee', 'number', (), u'退款金额'),
        ('out_biz_no', 'string', (64, ), u'商户业务号'),
        ('paytools_pay_amount', 'string', (512, ), u'支付金额信息'),
        ('extra_common_param', 'string', (256, ), u'业务透传参数')
    ),
    'alipay.wap.create.direct.pay.by.user': (
        ('notify_time', 'date', (), False, u'通知时间'),  # yyyy-MM-dd HH:mm:ss
        ('notify_type', 'string', (), False, u'通知类型'),
        ('notify_id', 'string', (), False, u'通知校验ID'),
        ('sign_type', 'string', (), False, u'签名方式'),  # DSA, RSA, MD5
        ('sign', 'string', (32, ), False, u'签名'),
        ('out_trade_no', 'string', (64, ), True, u'商户网站唯一订单号'),
        ('subject', 'string', (256, ), True, u'商品名称'),
        ('payment_type', 'string', (4, ), True, u'支付类型'),
        ('trade_no', 'string', (64, ), True, u'支付宝交易号'),
        ('trade_status', 'string', (), True, u'交易状态'),
        ('gmt_create', 'date', (), True, u'交易创建时间'),  # yyyy-MM-dd HH:mm:ss
        ('gmt_payment', 'date', (), True, u'交易付款时间'),  # yyyy-MM-dd HH:mm:ss
        ('gmt_close', 'date', (), True, u'交易关闭时间'),  # yyyy-MM-dd HH:mm:ss
        ('seller_email', 'string', (100, ), True, u'卖家支付宝账号'),  # email or mobile
        ('buyer_email', 'string', (100, ), True, u'买家支付宝账号'),  # email or mobile
        ('seller_id', 'string', (30, ), True, u'卖家支付宝账户号'),  # r'2088\d{12}'
        ('buyer_id', 'string', (30, ), True, u'买家支付宝账户号'),  # r'2088\d{12}'
        ('price', 'number', (), True, u'商品单价'),
        ('total_fee', 'number', (), True, u'交易金额'),
        ('quantity', 'number', (), True, u'购买数量'),
        ('body', 'string', (400, ), True, u'商品描述'),
        ('discount', 'number', (), True, u'折扣'),
        ('is_total_fee_adjust', 'string', (1, ), u'是否调整总价'),
        ('use_coupon', 'string', (1, ), u'是否使用红包买家'),
        ('refund_status', 'string', (), u'退款状态'),
        ('gmt_refund', 'date', (), u'退款时间')  # yyyy-MM-dd HH:mm:ss
    ),
    'alipay.dut.customer.agreement.page.sign': (
        ('notify_time', 'date', (), False, (2,), u'通知时间'),  # yyyy-MM-dd HH:mm:ss
        ('notify_type', 'string', (), False, (5, 'dut_user_sign'), u'通知类型'),
        ('notify_id', 'string', (), False, (2,), u'通知校验ID'),
        ('sign_type', 'string', (), False, (1,), u'签名方式'),
        ('sign', 'string', (), False, (2,), u'签名'),
        ('agreement_no', 'string', (), False, (2,), u'协议号'),
        ('product_code', 'string', (), False, (0,), u'签约产品码'),
        ('scene', 'string', (), False, (4, 'DEFAULT|DEFAULT'), u'签约场景'),
        # TEMP: never been effective
        # NORMAL
        # STOP
        ('status', 'string', (), False, (1,), u'协议状态'),
        ('alipay_user_id', 'string', (), False, (2,), u'支付宝用户号'),  # r'2088\d{12}'
        ('sign_time', 'string', (), False, (2,), u'签约时间'),
        ('sign_modify_time', 'string', (), False, (2,), u'签约修改时间'),
        ('valid_time', 'string', (), False, (2,), u'协议生效时间'),
        ('invalid_time', 'sting', (), False, (2,), u'协议失效时间'),
        ('partner_id', 'string', (16,), False, (0, 'partner'), u'合作者身份ID'),
        ('external_sign_no', 'string', (), True, (0,), u'商户签约号')
    )
}

VOCABULARY = {
    'alipay.acquire.createandpay': {
        'result_code': (
            'ORDER_FAIL',
            'ORDER_SUCCESS_PAY_SUCCESS',
            'ORDER_SUCCESS_PAY_FAIL',
            'ORDER_SUCCESS_PAY_INPROCESS',
            'UNKNOWN'
        ),
        'detail_error_code': {
            'TRADE_SETTLE_ERROR': u'分账信息校验失败',
            'TRADE_BUYER_NOT_MATCH': u'交易买家不匹配',
            'CONTEXT_INCONSISTENT': u'交易信息被篡改',
            'TRADE_HAS_SUCCESS': u'交易已经支付',
            'TRADE_HAS_CLOSE': u'交易已经关闭',
            'REASON_ILLEGAL_STATUS': u'交易的状态不合法',
            'EXIST_FORBIDDEN_WORD': u'订单信息中包含违禁词',
            'PARTNER_ERROR': u'合作伙伴信息不正确',
            'ACCESS_FORBIDDEN': u'没有权限使用该产品',
            'SELLER_NOT_EXIST': u'卖家不存在',
            'BUYER_NOT_EXIST': u'买家不存在',
            'BUYER_ENABLE_STATUS_FORBID': u'买家状态非法，无法继续交易',
            'BUYER_SELLER_EQUAL': u'卖家买家账号相同，不能进行交易',
            'INVALID_PARAMETER': u'参数无效',
            'UN_SUPPORT_BIZ_TYPE': u'不支持的业务类型',
            'INVALID_RECEIVE_ACCOUNT': u'卖家不在设置的收款账户列表中',
            'BUYER_PAYMENT_AMOUNT_DAY_LIMIT_ERROR': u'买家的付款日限额超限',
            'ERROR_BUYER_CERTIFY_LEVEL_LIMIT': u'买家未通过人行认证',
            'ERROR_SELLER_CERTIFY_LEVEL_LIMIT': u'卖家未通过人行认证',
            'CLIENT_VERSION_NOT_MATCH': u'钱包版本过低，请升级到最新版本后使用',
            'AUTH_NO_ERROR': u'授权号错误，可能的原因包括：'
                             u'授权号的商户跟当前请求商户不一致'
                             u'授权号的付款方跟当前请求中的付款方不一致'
                             u'授权号的可用资金比当前请求的解冻金额小'
                             u'授权状态不是已授权'
                             u'授权号的收款方跟当前请求中的收款方不一致',
            'BUYER_BANKCARD_BALANCE_NOT_ENOUGH': u'买家银行卡余额不足',
            'PULL_MOBILE_CASHIER_FAIL': u'唤起无线快捷收银台失败',
            'PAYMENT_FAIL': u'支付失败',
            'MOBILE_PAYMENT_SWITCH_OFF': u'用户无线支付开关关闭，无法进行支付'
        },
        'error_code': (
            'ILLEGAL_SIGN',
            'ILLEGAL_DYN_MD5_KEY',
            'ILLEGAL_ENCRYPT',
            'ILLEGAL_ARGUMENT',
            'ILLEGAL_SERVICE',
            'ILLEGAL_USER',
            'ILLEGAL_PARTNER',
            'ILLEGAL_EXTERFACE',
            'ILLEGAL_PARTNER_EXTERFACE',
            'ILLEGAL_SECURITY_PROFILE',
            'ILLEGAL_AGENT',
            'ILLEGAL_SIGN_TYPE',
            'ILLEGAL_CHARSET',
            'HAS_NO_PRIVILEGE',
            'INVALID_CHARACTER_SET',
            'SYSTEM_ERROR',
            'SESSION_TIMEOUT',
            'ILLEGAL_TARGET_SERVICE',
            'ILLEGAL_ACCESS_SWITCH_SYSTEM',
            'EXTERFACE_IS_CLOSED'
        ),
        'trade_status': (
            'WAIT_BUYER_PAY',
            'TRADE_CLOSED',
            'TRADE_SUCCESS',
            'TRADE_PENDING',
            'TRADE_FINISHED'
        )
    },
    'alipay.wap.create.direct.pay.by.user': {

    }
}
