import jwt
import datetime
from django.test import TestCase
from django.conf import settings
import pytest

from common.services.token import JWT

payload = {
    'one': 'two'
}
valid_payload = payload
expired_payload = payload
expired_payload['exp'] = datetime.datetime.now() - datetime.timedelta(minutes=15)

valid_token = jwt.encode(valid_payload, settings.SECRET_KEY, algorithm='HS256')
invalid_token_wrong_secret_key = jwt.encode(valid_payload, f'{settings.SECRET_KEY}_wrong', algorithm='HS256')
invalid_token_expired = jwt.encode(expired_payload, settings.SECRET_KEY, algorithm='HS256')

def test_valid_token_passes_decode():
    """A validly-signed and unexpired token will be parsed without fail."""
    token = JWT.decode(valid_token)
    assert token['one'] == valid_payload['one']

def test_token_with_wrong_secret_fails_decode():
    """A token signed with the wrong secret will fail."""
    with pytest.raises(jwt.InvalidTokenError) as error_invalid_token:
        JWT.decode(invalid_token_wrong_secret_key)
    assert 'token was invalid' in str(error_invalid_token.value)

def test_token_expired():
    """A token that is expired will fail."""
    with pytest.raises(jwt.InvalidTokenError) as error_expired_token:
        JWT.decode(invalid_token_expired)
    assert 'token was invalid' in str(error_expired_token.value)
