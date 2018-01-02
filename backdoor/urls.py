from django.conf.urls import url
from backdoor.views import alipayuser_detail


app_name = 'backdoor'
urlpatterns = [
    url(r'^alipayuser/(?P<user_id>\d+)', alipayuser_detail, name='alipayuser_detail')
]
