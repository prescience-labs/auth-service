from rest_framework import exceptions, serializers
from django.core import exceptions as ex
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from common.services.mailer import send_password_reset_email

User = get_user_model()

class PasswordResetInitSerializer(serializers.Serializer):
    """Initializes the password reset flow."""
    email = serializers.EmailField()

    class Meta:
        fields = ('email',)

    def validate(self, attrs):
        try:
            user: User = User.objects.get(email=attrs['email'])
            if user is not None:
                user.initiate_password_reset()
                email_message_result = send_password_reset_email(user)
                return {'email': attrs['email']}
            else:
                raise ex.ObjectDoesNotExist()
        except ex.ObjectDoesNotExist:
            raise exceptions.NotFound("That user wasn't found.")
        except:
            raise exceptions.APIException("We couldn't send the password reset email. Please reach out to us directly!")


class PasswordResetCompleteSerializer(serializers.Serializer):
    """Completes the password reset flow."""
    password = serializers.CharField()

    class Meta:
        fields = ('password',)

    def validate(self, attrs):
        try:
            # Step 1: Get user by token
            token       = attrs['token']
            password    = attrs['password']
            user        = get_object_or_404(User, password_reset_token=token)

            # Step 2: Reset password
            user.set_password(attrs['password'])
            user.password_reset_token = None
            user.password_reset_expiration = None
            user.save()

            # Step 3: Send success
            return {'email': user.email}
        except:
            raise exceptions.NotAcceptable("That password reset token wasn't valid.")
