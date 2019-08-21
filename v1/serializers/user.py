"""User Serializers"""
from django.contrib.auth import get_user_model
from rest_framework import serializers

#pylint: disable=invalid-name
User = get_user_model()
#pylint: enable=invalid-name

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    id = serializers.SerializerMethodField('get_user_id')

    class Meta:
        model = User
        fields = ['id', 'email']

    def get_user_id(self, obj):
        return obj.uid
