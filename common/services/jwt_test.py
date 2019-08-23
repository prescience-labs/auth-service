import jwt
from datetime import datetime, timedelta
from django.test import TestCase
from django.conf import settings
import pytest

from common.services.jwt import JWT, jwt_middleware

class TestJWTService:
    payload = {
        'one': 'two',
    }
    valid_token = ''
    invalid_token_wrong_secret_key = ''
    invalid_token_expired = ''

    def setUp(self):
        valid_payload = self.payload
        expired_payload = self.payload

        self.valid_token = jwt.encode(valid_payload, settings.SECRET_KEY)
        self.invalid_token_wrong_secret_key = jwt.encode(valid_payload, 'wrong_key')

        expired_payload['exp'] = datetime.utcnow()
        # self.invalid_token_expired = jwt.encode(payload, settings.SECRET_KEY)

    def test_valid_token_passes_decode(self):
        """A validly-signed and unexpired token will be parsed without fail."""
        token = JWT.decode(self.valid_token)
        self.assertEqual(token['one'], self.payload['one'])

    def test_token_with_wrong_secret_fails_decode(self):
        """A token signed with the wrong secret will fail."""
        with pytest.raises(jwt.InvalidTokenError) as error_invalid_token:
            decoded = JWT.decode(self.invalid_token_wrong_secret_key)
        assert 'token was invalid' in str(error_invalid_token.value)
