"""User Views"""
from rest_framework import exceptions, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from common.services.jwt import JWT
from v1.serializers import UserSerializer

#pylint: disable=invalid-name
User = get_user_model()
#pylint: enable=invalid-name

class UserList(APIView):
    """
    List all users.
    """
    queryset = User.objects.all()
    lookup_field = 'uid'

    def get(self, request, format=None):
        """Return a list of all users."""
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request':request})
        return Response(serializer.data)

class UserDetail(APIView):
    """
    Get a single user.
    """
    queryset = User.objects.all()
    lookup_field = 'uid'

    def get(self, request, uid, format=None):
        user = User.objects.get(uid=uid)
        serializer = UserSerializer(user, context={'request':request})
        return Response(serializer.data)

class CurrentUser(APIView):
    """
    Get details about the currently-authenticated user.
    """
    lookup_field = 'uid'

    def get(self, request, format=None):
        try:
            user = JWT.get_user_from_auth_header(request)
            if user is None:
                raise exceptions.NotFound
            serializer = UserSerializer(user, context={'request':request})
            return Response(serializer.data)
        except exceptions.NotFound:
            raise exceptions.NotFound('User was not found')
        except:
            raise Exception('Failed to get')
