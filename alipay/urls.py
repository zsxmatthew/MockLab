from django.conf.urls import url
from alipay.views import AlipayView


app_name = 'alipay'
urlpatterns = [
    url(r'^', AlipayView.as_view(), name='alipay')
]
