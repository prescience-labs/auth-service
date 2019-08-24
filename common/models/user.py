"""Custom User Model

This user model uses a uuid on the User.uid field.
"""
import uuid
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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

#pylint: disable=unused-argument
@receiver(pre_save, sender=User)
def force_username_email_parity(sender, instance, **kwargs):
    """
    Force the username to be the same as email for auth purposes.
    """
    instance.username = instance.email
