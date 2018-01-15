from django.conf.urls import url, include
from rest_framework import routers
from backdoor.views import AlipayUserViewSet  # , alipayuser_detail


router = routers.DefaultRouter()
router.register(r'alipayuser', AlipayUserViewSet)

app_name = 'backdoor'
urlpatterns = [
    url(r'^', include(router.urls)),
    # url(r'^alipayuser/(?P<user_id>\d+)', alipayuser_detail, name='alipayuser_detail')
]
