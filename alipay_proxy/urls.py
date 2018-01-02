from django.conf.urls import url
from alipay_proxy.views import AlipayProxyView


app_name = 'alipay_proxy'
urlpatterns = [
    url(r'^', AlipayProxyView.as_view(), name='alipay_proxy')
]
