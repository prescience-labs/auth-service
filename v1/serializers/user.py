"""User Serializers"""
#pylint: disable=too-few-public-methods,no-self-use
from django.contrib.auth import get_user_model
from rest_framework import serializers

from common.services.token import JWT

#pylint: disable=invalid-name
User = get_user_model()
#pylint: enable=invalid-name

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    id = serializers.SerializerMethodField('get_user_id')
    email = serializers.EmailField()

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

class CurrentUserSerializer(UserSerializer):
    permissions = serializers.SerializerMethodField('get_user_permissions')

    class Meta:
        """
        Meta class for the CurrentUser serializer.
        """
        model = User
        fields = ['id', 'email', 'permissions']
        read_only_fields = ['permissions']

    def get_user_permissions(self, obj):
        """
        Return permissions if:
            - the user requested is the same one authenticated, or
            - the authenticated user has permission ``can_view_permission``
        """
        user = JWT.get_user_from_auth_header(self.context['request'])
        if user is not None and user.uid == obj.uid:
            return obj.get_all_permissions()
        else:
            return []
