import jwt
import datetime

from django.test import TestCase
from django.conf import settings

from common.services.jwt import JWT

class JWTTests(TestCase):
    def setUp(self):
        self.payload = {
            'one': 'two',
        }
        self.valid_payload          = dict(self.payload)
        self.expired_payload        = dict(self.payload)
        self.expired_payload['exp'] = int(datetime.datetime.timestamp(datetime.datetime.utcnow() - datetime.timedelta(minutes=15)))

        self.valid_token                    = jwt.encode(self.valid_payload, settings.SECRET_KEY, algorithm='HS256').decode('UTF-8')
        self.invalid_token_wrong_secret_key = jwt.encode(self.valid_payload, f'{settings.SECRET_KEY}_wrong', algorithm='HS256').decode('UTF-8')
        self.invalid_token_expired          = jwt.encode(self.expired_payload, settings.SECRET_KEY, algorithm='HS256').decode('UTF-8')

    def test_valid_token_passes_decode(self):
        """A validly-signed and unexpired token will be parsed without fail."""
        token = JWT.decode(self.valid_token)
        self.assertEqual(token['one'], self.valid_payload['one'])

    def test_token_with_wrong_secret_fails_decode(self):
        """A token signed with the wrong secret will fail."""
        with self.assertRaises(jwt.InvalidTokenError) as error_invalid_token:
            JWT.decode(self.invalid_token_wrong_secret_key)
        self.assertIn('token was invalid', str(error_invalid_token.exception))

    def test_token_expired(self):
        """A token that is expired will fail."""
        with self.assertRaises(jwt.InvalidTokenError) as error_expired_token:
            JWT.decode(self.invalid_token_expired)
        self.assertIn('token was invalid', str(error_expired_token.exception))
