"""User Views"""
from rest_framework import generics
from django.contrib.auth import get_user_model
from app.serializers import UserSerializer

#pylint: disable=invalid-name
User = get_user_model()
#pylint: enable=invalid-name

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'uid'

class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'uid'
