import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

#pylint: disable=invalid-name
User = get_user_model()
#pylint: enable=invalid-name

USER_ID_CLAIM = 'user_id'

class JWT:
    @staticmethod
    def get_user_token(user):
        """
        Decide what goes into a token when a user requests one.
        """
        return JWT.encode({
            USER_ID_CLAIM: str(user.uid),
        })

    @staticmethod
    def decode(token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            return payload
        except:
            raise jwt.InvalidTokenError('The provided token was invalid')

    @staticmethod
    def get_user_from_jwt(token):
        try:
            if token is not None:
                payload = JWT.decode(token)
                user = User.objects.get(uid=payload[USER_ID_CLAIM])
                if user is not None:
                    return user
                else:
                    return None
            else:
                return None
        except:
            raise jwt.InvalidTokenError('The provided token was invalid')

    @staticmethod
    def encode(
        payload,
        token_expiration_days=settings.TOKEN_EXPIRATION_PERIOD,
    ):
        expiration_time = datetime.utcnow() + timedelta(days=token_expiration_days)
        payload['exp'] = expiration_time
        token = jwt.encode(payload, settings.SECRET_KEY)
        return token.decode('UTF-8')

    @staticmethod
    def refresh(token):
        """Attempt to refresh the provided token."""
        try:
            decoded = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(uid=decoded['user']['id'])
            return JWT.get_user_token(user)
        except jwt.ExpiredSignatureError:
            raise Exception('Token refresh failed. The provided token was expired.')
        except:
            raise Exception('Token refresh failed.')

def jwt_middleware(get_response):
    def middleware(request):
        try:
            token = request.headers['Authorization'] if request.headers['Authorization'] else None
            token = str.split(token)[1]
            user = JWT.get_user_from_jwt(token)

            # request._cached_user is used by
            # django.contrib.auth.get_user to
            # set the request.user object
            request._cached_user = user
        except:
            if not hasattr(request, '_cached_user'):
                request._cached_user = auth.get_user(request)

        response = get_response(request)
        return response

    return middleware
