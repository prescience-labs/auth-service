"""Custom User Model

This user model uses a uuid on the User.uid field.
"""
import uuid

from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """Custom User Model"""
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    token_valid_timestamp = models.DateTimeField(
        _('token valid timestamp'),
        null=True,
        blank=True,
        help_text=_('Tokens with an `iat` field before this timestamp will not validate.'),
    )

    # Password reset
    password_reset_token = models.UUIDField(_('password reset token'), null=True, blank=True)
    password_reset_expiration = models.DateTimeField(
        _('password reset expiration'),
        null=True,
        blank=True,
        help_text=_('Password reset tokens will only be valid until this timestamp.'),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def initiate_password_reset(self):
        self.password_reset_token = uuid.uuid4()
        self.password_reset_expiration = datetime.utcnow() + timedelta(minutes=settings.PASSWORD_RESET_EXPIRATION_MINUTES)
        self.save()


#pylint: disable=unused-argument
@receiver(pre_save, sender=User)
def force_username_email_parity(sender, instance, **kwargs):
    """
    Force the username to be the same as email for auth purposes.
    """
    instance.username = instance.email
