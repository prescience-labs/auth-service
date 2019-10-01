from rest_framework import serializers

from common.models import AppUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model   = AppUser
        fields  = '__all__'
