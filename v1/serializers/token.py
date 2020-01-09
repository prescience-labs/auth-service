from base64 import b64decode

from django.contrib.auth.models import Permission
from rest_framework import exceptions, serializers
from django.contrib.auth import authenticate, get_user_model

from common.models import Client
from common.services.jwt import JWT

User = get_user_model()

class TokenSerializer(serializers.Serializer):
    username_field = User.USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field]    = serializers.CharField()
        self.fields['password']             = serializers.CharField()

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


        team    = attrs.get('team', None)
        token   = JWT.get_user_token(self.user, team)
        return {'token':token}

    @classmethod
    def get_token(cls, user):
        raise NotImplementedError('Must implement `get_token` method for `TokenSerializer` subclasses')

class TokenObtainSerializer(TokenSerializer):
    def __init__(self, *args, **kwargs):
        self.fields['team'] = serializers.CharField(default=None)
        super().__init__(*args, **kwargs)

    @classmethod
    def get_token(cls, user, team):
        return JWT.get_user_token(user, team)

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

class ForceTokenObtainSerializer(TokenSerializer):
    """Force obtain a token for a given user

    For this authentication to work, the user must request using the Authorization header:

        Authorization: Basic <client_id>:<client_secret>

    Additionally, the client authenticating must have been granted the permission
    `can_force_user_login`.
    """
    def __init__(self, *args, **kwargs):
        self.fields['team']                 = serializers.CharField(default=None)
        self.fields[self.username_field]    = serializers.CharField()
        super().__init__(*args, **kwargs)
        del(self.fields['password'])

    def validate(self, attrs):
        try:
            request         = self.context['request']
            auth_header     = self.context['request'].headers.get('Authorization').split()[1]
            client_id       = auth_header.split(':')[0]
            client_secret   = auth_header.split(':')[1]

            client = Client.objects.get(client_id=client_id, client_secret=client_secret)
            print('GOT CLIENT:')
            print(client.id)
            if client.permissions.filter(codename='can_force_user_login').exists():
                user_email  = request.data['email']
                user        = User.objects.get(email=user_email)
                team        = attrs.get('team', None)
                token       = JWT.get_user_token(user, team)
                return {'token':token}
        except:
            raise exceptions.NotAuthenticated('The authentication was invalid')
