import jwt
from rest_framework import exceptions, generics, status
from rest_framework.response import Response

from common.services.jwt import JWT
from v1.serializers import TokenObtainSerializer, TokenRefreshSerializer, TokenVerifySerializer

class TokenViewBase(generics.GenericAPIView):
    permission_classes = ()
    authentication_classes = ()

    serializer_class = None

    def get_token_from_header(self, request):
        token = JWT.get_token_from_auth_header(request)
        return token

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except jwt.InvalidTokenError:
            raise exceptions.NotAuthenticated('The token was invalid')
        except:
            raise Exception('Error reading auth token')

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class TokenObtainView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = TokenObtainSerializer

token_obtain = TokenObtainView.as_view()

class TokenRefreshView(TokenViewBase):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """
    serializer_class = TokenRefreshSerializer


token_refresh = TokenRefreshView.as_view()

class TokenVerifyView(TokenViewBase):
    """
    Takes a token and indicates if it is valid.  This view provides no
    information about a token's fitness for a particular use.
    """
    serializer_class = TokenVerifySerializer

token_verify = TokenVerifyView.as_view()
