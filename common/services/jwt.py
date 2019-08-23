import logging

import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db.models import ObjectDoesNotExist

#pylint: disable=invalid-name
logger = logging.getLogger(__name__)
User = get_user_model()
#pylint: enable=invalid-name

USER_ID_CLAIM = 'user_id'

class JWT:
    @staticmethod
    def decode(token):
        logger.debug('JWT.decode() <<<<<<<<<<')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            logger.debug(f'PAYLOAD: {payload}')
            return payload
        except:
            logger.error('Unable to decode token')
            raise jwt.InvalidTokenError('The provided token was invalid')

    @staticmethod
    def encode(
        payload,
        token_expiration_days=settings.TOKEN_EXPIRATION_PERIOD,
    ):
        payload['iat'] = datetime.utcnow()
        payload['exp'] = datetime.utcnow() + timedelta(days=token_expiration_days)
        logger.debug(f'JWT encode, payload: {str(payload)}')
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


    @staticmethod
    def get_user_from_jwt(token):
        logger.debug('JWT.get_user_from_jwt() <<<<<<<<<<')
        try:
            if token is not None:
                payload = JWT.decode(token)
                try:
                    user = User.objects.get(uid=payload[USER_ID_CLAIM])
                    logger.debug(f'USER_ID: {user.uid}')
                    return user
                except ObjectDoesNotExist:
                    logger.debug('NO USER FOUND')
                    return None
                except:
                    logger.error('UNCAUGHT EXCEPTION')
                    return None
            else:
                logger.debug("Token doesn't exist.")
                None
        except:
            raise jwt.InvalidTokenError('The provided token was invalid')

    @staticmethod
    def get_user_token(user):
        """
        Decide what goes into a token when a user requests one.
        """
        return JWT.encode({
            USER_ID_CLAIM: str(user.uid),
        })

    @staticmethod
    def refresh_token(token):
        """
        Refresh a user's token if the token and user are valid.
        """
        try:
            user = JWT.get_user_from_jwt(token)
            if user is not None:
                return JWT.get_user_token(user)
            else:
                raise jwt.InvalidTokenError('The provided token was invalid')
        except:
            raise jwt.InvalidTokenError('The provided token was invalid')

    @staticmethod
    def get_token_from_auth_header(request):
        token = None
        try:
            token = request.headers['Authorization'] if request.headers['Authorization'] else None
            token = str.split(token)[1]
        except KeyError:
            pass
        return token

    @staticmethod
    def get_user_from_auth_header(request):
        token = JWT.get_token_from_auth_header(request)
        logger.debug(f'TOKEN: {token}')
        user = JWT.get_user_from_jwt(token)
        return user

def jwt_middleware(get_response):
    def middleware(request):
        try:
            if request._cached_user is not None:
                token = JWT.get_token_from_auth_header(request)
                user = JWT.get_user_from_jwt(token)
                if user is None:
                    user = AnonymousUser()
                # request._cached_user is used by
                # django.contrib.auth.get_user to
                # set the request.user object
                request._cached_user = user
        except:
            pass

        response = get_response(request)
        return response

    return middleware
