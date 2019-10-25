import logging

from django.contrib.auth.models import Permission
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from common.models import Client

logger  = logging.getLogger(__name__)

class ClientSerializer(serializers.ModelSerializer):
    permissions = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='codename',
    )

    class Meta:
        model   = Client
        exclude = ('client_secret',)
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
        ]
