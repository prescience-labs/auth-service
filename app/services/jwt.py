import jwt
from datetime import datetime, timedelta
from django.conf import settings

class JWT:
    @staticmethod
    def encode(
        payload,
        token_expiration_days=settings.TOKEN_EXPIRATION_PERIOD,
    ):
        expiration_time = datetime.utcnow() + timedelta(days=token_expiration_days)
        payload['exp'] = expiration_time
        payload['nbf'] = datetime.utcnow()
        token = jwt.encode(payload, settings.SECRET_KEY)
        return token.decode('UTF-8')
