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
    ),
    'alipay.dut.customer.agreement.query': (
        ('service', 'string', (), False, u'接口名称'),
        ('partner', 'string', (16,), False, u'合作者身份ID'),  # r'2088\d{14}'
        ('sign_type', 'string', (), False, u'签名方式'),  # DSA/RSA/MD5
        ('sign', 'string', (), False, u'签名'),
        ('_input_charset', 'string', (), True, u'参数编码字符集'),
        ('product_code', 'string', (64,), False, u'产品代码'),
        ('alipay_user_id', 'string', (), True, u'用户支付宝用户号'),
        ('alipay_logon_id', 'string', (100,), True, u'用户支付宝账号'),
        ('scene', 'string', (100,), True, u'场景'),
        ('app_id', 'string', (), True, u'商户接入公众平台时对应的appid'),
        ('external_sign_no', 'string', (32,), True, u'商户签约号')
    ),
    'alipay.trade.pay': (
        # public
        ('app_id', 'string', (32,), False, u'支付宝分配给开发者的应用ID'),
        ('method', 'string', (128,), False, u'接口名称'),
        ('format', 'string', (40,), True, u'仅支持JSON'),
        ('charset', 'string', (10,), False, u'请求使用的编码格式'),  # utf-8/gbk/gb2312
        ('sign_type', 'string', (10,), False, u'商户生成签名字符串所用的签名算法类型'),  # RSA2/RSA
        ('sign', 'string', (344,), False, u'商户请求参数的签名串'),
        ('timestamp', 'string', (19,), False, u'发送请求的时间'),  # yyyy-MM-dd HH:MM:SS
        ('version', 'string', (3,), False, u'调用的接口版本'),  # 1.0
        ('notify_url', 'string', (256,), True, u'支付宝服务器主动通知商户服务器里指定的页面'),
        ('app_auth_token', 'string', (40,), True, u'应用授权'),
        ('biz_content', 'string', (), False, u'请求参数的集合'),
        # request
        ('out_trade_no', 'string', (64,), False, u'商户订单号'),
        ('scene', 'string', (32,), False, u'支付场景'),
        ('auth_code', 'string', (32,), False, u'支付授权码'),
        ('product_code', 'string', (32,), True, u'销售产品码'),
        ('subject', 'string', (256,), False, u'订单标题'),
        ('buyer_id', 'string', (28,), True, u'买家的支付宝用户ID'),
        ('seller_id', 'string', (28,), True, u'商户签约账号对应的支付宝用户ID'),
        ('total_amount', 'number', (9, 2), True, u'订单总金额'),
        ('discountable_amount', 'number', (9, 2), True, u'参与优惠计算的金额'),
        ('body', 'string', (128,), True, u'订单描述'),
        ('goods_detail', 'json', (), True, u'订单包含的商品列表信息'),
        ('operator_id', 'string', (28,), True, u'商户操作员编号'),
        ('store_id', 'string', (32,), True, u'商户门店编号'),
        ('terminal_id', 'string', (32,), True, u'商户机具终端编号'),
        ('extend_params', 'json', (), True, u'业务扩展参数'),
        ('timeout_express', 'string', (6,), True, u'该笔订单允许的最晚付款时间')
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
    ),
    'alipay.dut.customer.agreement.query': (
        ('is_success', 'string', (), False, (2,), u'是否成功'),  # T/F
        ('sign_type', 'string', (), True, (1,), u'签名方式'),  # DSA/RSA/MD5
        ('sign', 'sring', (), True, (2,), u'签名'),
        ('error', 'string', (), True, (2,), u'错误代码'),
        ('pricipal_type', 'string', (), False, (1,), u'签约主体类型'),  # CARD/CUSTOMER
        ('principal_id', 'stirng', (), False, (2,), u'签约主体标识'),
        ('product_code', 'string',(), False, (0,), u'签约产品码'),
        ('scene', 'string', (), False, (0, 'DEFAULT|DEFAULT'), u'签约产品场景'),
        ('thirdpart_type', 'string', (), False, (5, 'PARTNER'), u'三方协议第三方主体类型'),
        ('thirdpart_id', 'string', (), False, (5, 'PARTNER_TAOBAO_ORDER'), u'三方协议第三方主体'),
        ('status', 'string', (), False, (3,), u'协议状态'),
        ('valid_time', 'date', (), False, (3,), u'生效时间'),  # yyyy-MM-dd HH:MM:SS
        ('invalid_time', 'date', (), False, (3,), u'失效时间'),  # yyyy-MM-dd HH:MM:SS
        ('sign_time', 'date', (), False, (3,), u'签约时间'),  # yyyy-MM-dd HH:MM:SS
        ('sign_modify_time', 'date', (), False, (3,), u'签约修改时间'),  # yyyy-MM-dd HH:MM:SS
        ('external_sign_no', 'string', (), True, (3,), u'商户签约号'),
        ('agreement_detail', 'string', (), True, (3,), u'协议细则')
    ),
    'alipay.trade.pay': (
        # public
        ('code', 'string', (), False, (2,), u'网关返回码'),
        ('msg', 'string', (), False, (2,), u'网关返回码描述'),
        ('sub_code', 'string', (), True, (2,), u'业务返回码'),
        ('sub_msg', 'string', (), True, (2,), u'业务返回码描述'),
        ('sign', 'string', (), False, (2,), u'签名'),
        # response
        ('trade_no', 'string', (64,), False, u'支付宝交易号'),
        ('out_trade_no', 'string', (64,), False, u'商户订单号'),
        ('buyer_logon_id', 'string', (100,), False, u'买家支付宝账号'),
        ('total_amount', 'number', (9, 2), False, u'交易金额'),
        ('receipt_amount', 'string', (9, 2), False, u'实收金额'),
        ('buyer_pay_amount', 'number', (9, 2), True, u'买家付款的金额'),
        ('point_amount', 'number', (9, 2), True, u'使用积分宝付款的金额'),
        ('invoice_amount', 'number', (9, 2), True, u'交易中可给用户开具发票的金额'),
        ('gmt_payment', 'date', (32,), False, u'交易支付时间'),
        ('fund_bill_list', 'json', (), False, u'交易支付使用的资金渠道'),
        ('card_balance', 'number', (9, 2), True, u'支付宝卡余额'),
        ('store_name', 'string', (512,), True, u'发生支付交易的商户门店名称'),
        ('buyer_user_id', 'string', (28,), False, u'买家在支付宝的用户id'),
        ('discount_goods_detail', 'string', (1024,), True, u'本次交易支付所使用的单品券优惠的商品优惠信息'),
        ('voucher_detail_list', 'json', (), True, u'本交易支付时使用的所有优惠券信息'),
        ('business_params', 'string', (512,), True, u'商户传入业务信息'),
        ('buyer_user_type', 'string', (18,), True, u'买家用户类型')
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
    },
    'alipay.trade.pay': {
        'sub_code': {
            # sub_code: (sub_msg, code)
            'ACQ.SYSTEM_ERROR': (u'接口返回错误', '40004'),
            'ACQ.INVALID_PARAMETER': (u'参数无效', '40004'),
            'ACQ.ACCESS_FORBIDDEN': (u'无权限使用接口', '40004'),
            'ACQ.EXIST_FORBIDDEN_WORD': (u'订单信息中包含违禁词', '40004'),
            'ACQ.PARTNER_ERROR': (u'应用APP_ID填写错误', '40004'),
            'ACQ.TOTAL_FEE_EXCEED': (u'订单总金额超过限额', '40004'),
            'ACQ.PAYMENT_AUTH_CODE_INVALID': (u'支付授权码无效', '40004'),
            'ACQ.CONTEXT_INCONSISTENT': (u'交易信息被篡改', '40004'),
            'ACQ.TRADE_HAS_SUCCESS': (u'交易已被支付', '40004'),
            'ACQ.TRADE_HAS_CLOSE': (u'交易已经关闭', '40004'),
            'ACQ.BUYER_BALANCE_NOT_ENOUGH': (u'买家余额不足', '40004'),
            'ACQ.BUYER_BANKCARD_BALANCE_NOT_ENOUGH': (u'用户银行卡余额不足', '40004'),
            'ACQ.ERROR_BALANCE_PAYMENT_DISABLE': (u'余额支付功能关闭', '40004'),
            'ACQ.BUYER_SELLER_EQUAL': (u'买卖家不能相同', '40004'),
            'ACQ.TRADE_BUYER_NOT_MATCH': (u'交易买家不匹配', '40004'),
            'ACQ.BUYER_ENABLE_STATUS_FORBID': (u'买家状态非法', '40004'),
            'ACQ.PULL_MOBILE_CASHIER_FAIL': (u'唤起移动收银台失败', '40004'),
            'ACQ.MOBILE_PAYMENT_SWITCH_OFF': (u'用户的无线支付开关关闭', '40004'),
            'ACQ.PAYMENT_FAIL': (u'支付失败', '40004'),
            'ACQ.BUYER_PAYMENT_AMOUNT_DAY_LIMIT_ERROR': (u'买家付款日限额超限', '40004'),
            'ACQ.BEYOND_PAY_RESTRICTION': (u'商户收款额度超限', '40004'),
            'ACQ.BEYOND_PER_RECEIPT_RESTRICTION': (u'商户收款金额超过月限额', '40004'),
            'ACQ.BUYER_PAYMENT_AMOUNT_MONTH_LIMIT_ERROR': (u'买家付款月额度超限', '40004'),
            'ACQ.SELLER_BEEN_BLOCKED': (u'商家账号被冻结', '40004'),
            'ACQ.ERROR_BUYER_CERTIFY_LEVEL_LIMIT': (u'买家未通过人行认证', '40004'),
            'ACQ.PAYMENT_REQUEST_HAS_RISK': (u'支付有风险', '40004'),
            'ACQ.NO_PAYMENT_INSTRUMENTS_AVAILABLE': (u'没用可用的支付工具', '40004'),
            'ACQ.USER_FACE_PAYMENT_SWITCH_OFF': (u'用户当面付付款开关关闭', '40004'),
            'ACQ.INVALID_STORE_ID': (u'商户门店编号无效', '40004'),
            'ACQ.SUB_MERCHANT_CREATE_FAIL': (u'二级商户创建失败', '40004'),
            'ACQ.SUB_MERCHANT_TYPE_INVALID': (u'二级商户类型非法', '40004'),
            'ACQ.AGREEMENT_NOT_EXIST': (u'用户协议不存在', '40004'),
            'ACQ.AGREEMENT_INVALID': (u'用户协议失效', '40004'),
            'ACQ.AGREEMENT_STATUS_NOT_NORMAL': (u'用户协议状态非NORMAL', '40004'),
            'ACQ.MERCHANT_AGREEMENT_NOT_EXIST': (u'商户协议不存在', '40004'),
            'ACQ.MERCHANT_AGREEMENT_INVALID': (u'商户协议已失效', '40004'),
            'ACQ.MERCHANT_STATUS_NOT_NORMAL': (u'商户协议状态非正常状态', '40004')
        }
    },
    'public': {
        'code': {
            '10000': u'接口调用成功，调用结果请参考具体的API文档所对应的业务返回参数',
            '20000': u'服务不可用',
            '20001': u'授权权限不足',
            '40001': u'缺少必选参数',
            '40002': u'非法的参数',
            '40004': u'业务处理失败',
            '40006': u'权限不足'
        },
        'sub_code': {
            # sub_code: (sub_msg, code)
            'isp.unknow-error': (u'服务暂不可用（业务系统不可用）', '10000'),
            'aop.unknow-error': (u'服务暂不可用（网关自身的未知错误）', '20000'),
            'aop.invalid-auth-token': (u'无效的访问令牌', '20001'),
            'aop.auth-token-time-out': (u'访问令牌已过期', '20001'),
            'aop.invalid-app-auth-token	': (u'无效的应用授权令牌', '20001'),
            'aop.invalid-app-auth-token-no-api': (u'商户未授权当前接口', '20001'),
            'aop.app-auth-token-time-out': (u'应用授权令牌已过期', '20001'),
            'aop.no-product-reg-by-partner': (u'商户未签约任何产品', '20001'),
            'isv.missing-method': (u'缺少方法名参数', '40001'),
            'isv.missing-signature': (u'缺少签名参数', '40001'),
            'isv.missing-signature-type': (u'缺少签名类型参数', '40001'),
            'isv.missing-signature-key': (u'缺少签名配置', '40001'),
            'isv.missing-app-id': (u'缺少appId参数', '40001'),
            'isv.missing-timestamp': (u'缺少时间戳参数', '40001'),
            'isv.missing-version': (u'缺少版本参数', '40001'),
            'isv.decryption-error-missing-encrypt-type': (u'解密出错, 未指定加密算法', '40001'),
            'isv.invalid-parameter': (u'参数无效', '40002'),
            'isv.upload-fail': (u'文件上传失败', '40002'),
            'isv.invalid-file-extension': (u'文件扩展名无效', '40002'),
            'isv.invalid-file-size': (u'文件大小无效', '40002'),
            'isv.invalid-method': (u'不存在的方法名', '40002'),
            'isv.invalid-format': (u'无效的数据格式', '40002'),
            'isv.invalid-signature-type': (u'无效的签名类型', '40002'),
            'isv.invalid-signature': (u'无效签名', '40002'),
            'isv.invalid-encrypt-type': (u'无效的加密类型', '40002'),
            'isv.invalid-encrypt': (u'解密异常', '40002'),
            'isv.invalid-app-id': (u'无效的appId参数', '40002'),
            'isv.invalid-timestamp': (u'非法的时间戳参数', '40002'),
            'isv.invalid-charset': (u'字符集错误', '40002'),
            'isv.invalid-digest': (u'摘要错误', '40002'),
            'isv.decryption-error-not-valid-encrypt-type': (u'解密出错，不支持的加密算法', '40002'),
            'isv.decryption-error-not-valid-encrypt-key': (u'解密出错, 未配置加密密钥或加密密钥格式错误', '40002'),
            'isv.decryption-error-unknown': (u'解密出错，未知异常', '40002'),
            'isv.missing-signature-config': (u'验签出错, 未配置对应签名算法的公钥或者证书', '40002'),
            'isv.not-support-app-auth': (u'本接口不支持第三方代理调用', '40002'),
            'isv.insufficient-isv-permissions': (u'ISV权限不足', '40006'),
            'isv.insufficient-user-permissions': (u'用户权限不足', '40006')
        },
        'channel': [
            ('COUPON', u'支付宝红包'),
            ('ALIPAYACCOUNT', u'支付宝账户'),
            ('POINT', u'集分宝'),
            ('DISCOUNT', u'折扣券'),
            ('PCARD', u'预付卡'),
            ('MCARD', u'商家储值卡'),
            ('MDISCOUNT', u'商户优惠券'),
            ('MCOUPON', u'商户红包'),
            ('PCREDIT', u'	蚂蚁花呗')
        ]
    }
}
