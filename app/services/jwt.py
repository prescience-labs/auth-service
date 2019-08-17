import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model

#pylint: disable=invalid-name
User = get_user_model()
#pylint: enable=invalid-name

class JWT:
    @staticmethod
    def get_user_token(user):
        """
        Decide what goes into a token when a user requests one.
        """
        return JWT.encode({
            'user': {
                'id': str(user.uid),
                'permissions': list(user.get_all_permissions()),
            },
        })

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
        decoded = jwt.decode(token, settings.SECRET_KEY)
        user = User.objects.get(uid=decoded['user']['id'])
        return JWT.get_user_token(user)
