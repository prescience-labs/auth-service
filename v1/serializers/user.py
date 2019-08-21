"""User Serializers"""
#pylint: disable=too-few-public-methods,no-self-use
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
        """
        Meta class for the User serializer.
        """
        model = User
        fields = ['id', 'email']

    def get_user_id(self, obj):
        """
        Return the user.uid instead of user.id
        """
        return obj.uid
