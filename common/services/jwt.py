import logging

import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db.models import ObjectDoesNotExist

logger = logging.getLogger(__name__)
User = get_user_model()

USER_ID_CLAIM = 'user_id'

class JWT:
    @staticmethod
    def decode(token):
        """Decode the given token with the secret key.
        This does not perform any user validation, only signature validation.
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            logger.debug(f'PAYLOAD: {payload}')
            return payload
        except:
            logger.error('Unable to decode token')
            raise jwt.InvalidTokenError('The provided token was invalid')

    @staticmethod
    def encode(
        payload,
        token_expiration_days=settings.TOKEN_EXPIRATION_DAYS,
    ):
        payload['iat'] = datetime.utcnow()
        payload['exp'] = datetime.utcnow() + timedelta(days=token_expiration_days)
        logger.debug(f'JWT encode, payload: {str(payload)}')
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token.decode('UTF-8')

    @staticmethod
    def refresh(token):
        """Attempt to refresh the provided token."""
        try:
            user = JWT.get_user_from_jwt(token)
            return JWT.get_user_token(user)
        except jwt.ExpiredSignatureError:
            raise Exception('Token refresh failed. The provided token was expired.')
        except:
            raise Exception('Token refresh failed.')


    @staticmethod
    def get_user_from_jwt(token):
        try:
            if token is not None:
                payload = JWT.decode(token)
                try:
                    user = User.objects.get(id=payload[USER_ID_CLAIM])
                    jwt_timestamp = payload['iat']
                    user_token_valid_timestamp = None if user.token_valid_timestamp is None else datetime.timestamp(user.token_valid_timestamp)
                    if user_token_valid_timestamp is not None and user_token_valid_timestamp >= jwt_timestamp:
                        raise jwt.InvalidTokenError
                    logger.debug(f'USER_ID: {user.id}')
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
            USER_ID_CLAIM: str(user.id),
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
        """Extracts the user from the Authorization header

        Expects the authorization header to be formatted like

        ```
        Authorization "Bearer <token>"
        ```
        """
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
    """Adds the current user to request._cached_user

    If no user is logged in, it adds AnonymousUser to the request.
    """
    def middleware(request):
        response = get_response(request)
        try:
            user = JWT.get_user_from_auth_header(request)
            request._cached_user = user if user else AnonymousUser()
        except:
            request._cached_user = AnonymousUser()
        logger.info(f'Current user: {request._cached_user}')
        return response
    return middleware
