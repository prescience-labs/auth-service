"""User Views"""
from rest_framework import exceptions, generics, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response

from common.models import AppUser
from v1.serializers import UserSerializer

class UserList(generics.ListAPIView):
    queryset = AppUser.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = AppUser.objects.all()
    serializer_class = UserSerializer
