from rest_framework import exceptions, serializers
from django.contrib.auth import authenticate, get_user_model

from common.services.jwt import JWT

User = get_user_model()

class TokenSerializer(serializers.Serializer):
    username_field = User.USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = serializers.CharField()

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if self.user is None or not self.user.is_active:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        token = JWT.get_user_token(self.user)
        return {'token':token}

    @classmethod
    def get_token(cls, user):
        raise NotImplementedError('Must implement `get_token` method for `TokenSerializer` subclasses')

class TokenObtainSerializer(TokenSerializer):
    @classmethod
    def get_token(cls, user):
        return JWT.get_user_token(user)

    def validate(self, attrs):
        data = super().validate(attrs)
        return data

class TokenRefreshSerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, attrs):
        token = JWT.refresh_token(attrs['token'])
        return {'token':token}

class TokenVerifySerializer(serializers.Serializer):
    token = serializers.CharField()

    def validate(self, attrs):
        try:
            user = JWT.get_user_from_jwt(attrs['token'])
            if user is not None:
                return {'user_id':user.uid}
            else:
                raise exceptions.NotAuthenticated('The token was invalid')
        except:
            raise exceptions.NotAuthenticated('The token was invalid')
