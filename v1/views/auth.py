from rest_framework import exceptions, generics, mixins, status

from v1.serializers import AuthPasswordResetSerializer

class AuthPasswordResetInit(generics.CreateAPIView):
    serializer_class = AuthPasswordResetSerializer

class AuthPasswordResetFinal(generics.UpdateAPIView):
    pass
