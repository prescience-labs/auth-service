import logging

import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db.models import ObjectDoesNotExist

from common.models import Team

logger = logging.getLogger(__name__)
User = get_user_model()

USER_ID_CLAIM = 'user_id'
TEAM_ID_CLAIM = 'team_id'

class JWT:
    @staticmethod
    def decode(token):
        """Decode the given token with the secret key

        This does not perform any user validation, only signature validation.

        Args:
        - token (string): The token to decode

        Raises:
        - jwt.InvalidTokenError: If the token is invalid (usually signed with a different key)

        Returns:
        - dict: The token payload
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms='HS256')
            logger.debug(f'PAYLOAD: {payload}')
            return payload
        except:
            logger.warning('Unable to decode token')
            raise jwt.InvalidTokenError('The provided token was invalid')

    @staticmethod
    def encode(
        payload,
        token_expiration_days=settings.TOKEN_EXPIRATION_DAYS,
    ):
        payload['iat']  = datetime.utcnow()
        payload['exp']  = datetime.utcnow() + timedelta(days=token_expiration_days)
        token           = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        logger.debug(f'JWT encode, payload: {str(payload)}')
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
        """Gets a user from the token

        Args:
        - token (string): The token to decode. Should be signed with the correct secret key.

        Raises:
        - jwt.InvalidTokenError: If the user's `token_valid_timestamp` is set before the token's `iat` timestamp.

        Returns:
        - User: The user from the token
        - (None): Returned if anything failed
        """
        try:
            if token is not None:
                payload = JWT.decode(token)
                try:
                    user            = User.objects.get(id=payload[USER_ID_CLAIM])
                    jwt_timestamp   = payload['iat']

                    # Check to see if user's token_valid_timestamp field is set and if it is set for a date before the iat date
                    user_token_valid_timestamp = None if user.token_valid_timestamp is None else datetime.timestamp(user.token_valid_timestamp)
                    if user_token_valid_timestamp is not None and user_token_valid_timestamp >= jwt_timestamp:
                        logger.info("The user's token_valid_timestamp was before the token's iat timestamp")
                        raise jwt.InvalidTokenError

                    logger.debug(f'Decoded a token with user_id: {user.id}')
                    return user
                except ObjectDoesNotExist:
                    logger.debug('NO USER FOUND')
                except Exception as e:
                    logger.error(e)
            else:
                logger.debug("Token doesn't exist.")
        except:
            raise jwt.InvalidTokenError('The provided token was invalid')
        return None

    @staticmethod
    def get_user_token(user, team=None):
        """
        Decide what goes into a token when a user requests one.
        """
        default_team_id = None
        try:
            if team:
                if type(team) is str:
                    logger.debug(f'Team sent as a string: {team}. Converting to a Team object...')
                    team = Team.objects.get(pk=team)

                if team in user.teams.all():
                    default_team_id = str(team.id)
                else:
                    logger.warning(f"Tried to create an auth token with user {user} and team {team} but that user doesn't belong to that team.")
            else:
                default_team_id = str(user.default_team.id)
        except Exception as e:
            logger.info(f"User {user} doesn't have a team to serialize (error thrown: {e})")
        return JWT.encode({
            USER_ID_CLAIM: str(user.id),
            TEAM_ID_CLAIM: default_team_id,
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
    def get_token_from_request(request):
        """Extracts the user from the Authorization header

        Expects the authorization header to be formatted like

        ```
        Authorization "Bearer <token>"
        ```
        """
        token = None
        try:
            header = request.headers.get('Authorization').split()
            if header[0].lower() == 'bearer':
                token = header[1]
        except KeyError:
            pass
        return token

    @staticmethod
    def get_user_from_request(request):
        token = JWT.get_token_from_request(request)
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
            user = JWT.get_user_from_request(request)
            request._cached_user = user if user else AnonymousUser()
        except:
            request._cached_user = AnonymousUser()
        logger.info(f'Current user: {request._cached_user}')
        return response
    return middleware
