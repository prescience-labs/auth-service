from rest_framework import exceptions, serializers
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from common.services.mailer import send_password_reset_email

User = get_user_model()

class AuthPasswordResetSerializer(serializers.Serializer):
    """Allows a user to reset their password."""
    email = serializers.EmailField()
    message = serializers.CharField(read_only=True)

    class Meta:
        fields = ('email', 'message',)

    def create(self, validated_data):
        # Step 1: Check for existing user.
        user = get_object_or_404(User, email=validated_data.get('email'))

        # Step 2: Set user token and expiration
        user.initiate_password_reset()

        # Step 3: Send a message
        email = send_password_reset_email(user)
        return validated_data
