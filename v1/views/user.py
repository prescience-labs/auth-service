"""User Views"""
from rest_framework import exceptions, generics, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response

from common.models import AppUser
from v1.serializers import CreateUserSerializer, UserSerializer

class Users(APIView):
    def post(self, request):
        """Creates a new user."""
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.create(serializer.validated_data)
            return Response(result, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserList(generics.ListCreateAPIView):
    queryset = AppUser.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = AppUser.objects.all()
    serializer_class = UserSerializer
