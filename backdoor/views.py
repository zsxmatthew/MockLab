# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from alipay.models import AlipayUser
from backdoor.serializers import AlipayUserSerializer


@api_view(['GET', 'POST', 'PUT'])
def alipayuser_detail(request, user_id):
    print 'alipayuser_detail'.center(40, '-')
    data = {'user_id': user_id}
    data.update(request.data.dict())
    try:
        user = AlipayUser.objects.get(user_id=user_id)
    except AlipayUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':  # get
        serializer = AlipayUserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'POST':  # create
        serializer = AlipayUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':  # update
        serializer = AlipayUserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
