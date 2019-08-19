"""Auth Views"""
from django.contrib.auth import authenticate
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from app.serializers import TokenSerializer

class Token(APIView):
    def post(self, request, format=None):
        print(request.data)
        username = request.data['email']
        password = request.data['password']
        user = authenticate(
            username=username,
            password=password
        )
        if user is not None:
            token = TokenSerializer(user).token
            return Response({'token':token}, status=status.HTTP_201_CREATED)
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise exceptions.AuthenticationFailed('Incorrect credentials.')
