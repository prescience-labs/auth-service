from rest_framework import serializers

from common.models import AppUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        """
        Meta class for the User serializer.
        """
        model = AppUser
        fields = ('id', 'provider_id',)
