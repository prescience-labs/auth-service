"""User Views"""
from rest_framework import exceptions, generics, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from common.services.token import JWT
from v1.serializers import UserSerializer, CurrentUserSerializer

#pylint: disable=invalid-name
User = get_user_model()
#pylint: enable=invalid-name

class UserList(generics.ListCreateAPIView):
    """
    List all users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'uid'

class UserDetail(generics.RetrieveAPIView):
    """
    Get a single user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'uid'

class CurrentUser(generics.GenericAPIView):
    """
    Get details about the currently-authenticated user.
    """
    lookup_field = 'uid'

    def get(self, request):
        try:
            print('GETTING USER FROM AUTH HEADER')
            user = JWT.get_user_from_auth_header(request)
            print(user)
            if user is None or user.id is None:
                print('!!!!!!!!!!!!')
                raise exceptions.NotFound()
            serializer = CurrentUserSerializer(user, context={'request':request})
            return Response(serializer.data)
        except:
            raise exceptions.NotFound('User was not found')
