from django.conf import settings
import requests
from rest_framework import serializers

from common.services.auth0 import Auth0Client

class CreateUserSerializer(serializers.Serializer):
    connection      = serializers.CharField(write_only=True, default='Username-Password-Authentication')
    email           = serializers.CharField()
    password        = serializers.CharField(write_only=True)
    email_verified  = serializers.BooleanField(required=False, default=False)
    app_metadata    = serializers.DictField(read_only=True)
    user_metadata   = serializers.DictField(read_only=True)
    user_id         = serializers.CharField(read_only=True)
    name            = serializers.CharField(read_only=True)
    nickname        = serializers.CharField(read_only=True)
    identities      = serializers.ListField(read_only=True,
        child=serializers.DictField(read_only=True),
    )
    created_at      = serializers.CharField(read_only=True)
    updated_at      = serializers.CharField(read_only=True)

    class Meta:
        fields = (
            'connection',
            'email',
            'password',
            'email_verified',
            'app_metadata',
            'user_metadata',
            'user_id',
            'name',
            'nickname',
            'identities',
            'created_at',
            'updated_at',
        )

    def create(self, validated_data):
        client = Auth0Client()
        result = client.post('/users', validated_data)
        return result

    def save(self, **kwargs):
        print('saving')
        self.create(self.validated_data)
        return super().save(**kwargs)
