from datetime import datetime

from rest_framework import exceptions, serializers
from django.core import exceptions as ex
from django.contrib.auth import get_user_model
from django.db.models import Q

from common.services.mailer import send_password_reset_email

User = get_user_model()

class PasswordResetBaseSerializer(serializers.Serializer):
    email   = serializers.EmailField()
    token   = serializers.UUIDField()

    class Meta:
        fields = ('email', 'token',)

    @staticmethod
    def get_user_from_token(token) -> User:
        user = User.objects.filter(password_reset_token=token)
        user = user.filter(password_reset_expiration__gte=datetime.utcnow())
        return user[0]

class PasswordResetInitSerializer(PasswordResetBaseSerializer):
    token   = serializers.UUIDField(read_only=True)

    def validate(self, attrs):
        try:
            user: User = User.objects.get(email=attrs['email'])
            if user is not None:
                user.initiate_password_reset()
                email_message_result = send_password_reset_email(user)
                return {
                    'email': user.email,
                    'token': user.password_reset_token,
                }
            else:
                raise ex.ObjectDoesNotExist()
        except ex.ObjectDoesNotExist:
            raise exceptions.NotFound("That user wasn't found.")
        except:
            raise exceptions.APIException("We couldn't send the password reset email. Please reach out to us directly!")


class PasswordResetCompleteSerializer(PasswordResetBaseSerializer):
    email       = serializers.CharField(read_only=True)
    password    = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            token       = attrs['token']
            password    = attrs['password']
            user        = PasswordResetBaseSerializer.get_user_from_token(token)

            if user is not None:
                user.set_password(attrs['password'])
                user.password_reset_token = None
                user.password_reset_expiration = None
                user.save()
                return {
                    'email': user.email,
                }
            else:
                raise ex.ObjectDoesNotExist("That password reset token wasn't valid.")
        except ex.ObjectDoesNotExist:
            raise exceptions.NotFound("That password reset token wasn't valid.,")
        except:
            raise exceptions.NotAcceptable("That password reset token wasn't valid.")
