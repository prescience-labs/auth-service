import jwt
from django.core.exceptions import PermissionDenied
from rest_framework import exceptions, generics, status
from rest_framework.response import Response

from common.services.jwt import JWT
from v1.serializers import TokenObtainSerializer, TokenRefreshSerializer, TokenVerifySerializer

class TokenViewBase(generics.GenericAPIView):
    permission_classes = ()
    authentication_classes = ()

    serializer_class = None

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except jwt.InvalidTokenError:
            raise exceptions.NotAuthenticated('The token was invalid. Try grabbing a new token.')
        except PermissionDenied:
            raise exceptions.NotAuthenticated('The auth credentials provided were invalid')
        except:
            raise exceptions.NotAuthenticated('The auth credentials provided were invalid')

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class TokenObtainView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = TokenObtainSerializer

class TokenRefreshView(TokenViewBase):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """
    serializer_class = TokenRefreshSerializer

class TokenVerifyView(TokenViewBase):
    """
    Takes a token and indicates if it is valid.  This view provides no
    information about a token's fitness for a particular use.
    """
    serializer_class = TokenVerifySerializer
