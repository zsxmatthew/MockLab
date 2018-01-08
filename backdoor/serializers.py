# --*-- coding: utf-8 --*--
from rest_framework import serializers

from alipay.models import AlipayUser


class AlipayUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlipayUser
        fields = ('user_id', 'is_success', 'other_options')
