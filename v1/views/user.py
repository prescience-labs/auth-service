from django.contrib.auth import get_user_model
from rest_framework import exceptions, generics, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response

from common.services.jwt import JWT
from v1.serializers import UserSerializer, UserDetailSerializer

User = get_user_model()

class UserList(generics.ListCreateAPIView):
    queryset            = User.objects.filter(is_active=True)
    serializer_class    = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset            = User.objects.filter(is_active=True)
    serializer_class    = UserDetailSerializer

class UserFromTokenDetail(generics.RetrieveAPIView):
    serializer_class    = UserDetailSerializer

    def get_queryset(self):
        token               = JWT.get_token_from_request(self.request)
        payload             = JWT.decode(token)
        self.kwargs['pk']   = payload['user_id']
        return User.objects.filter(is_active=True)
