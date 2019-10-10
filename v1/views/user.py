from django.contrib.auth import get_user_model
from rest_framework import exceptions, generics, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response

from v1.serializers import UserSerializer, UserDetailSerializer

User = get_user_model()

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserDetailSerializer
