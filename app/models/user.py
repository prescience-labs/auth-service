import uuid
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save
from django.db import models
from django.dispatch import receiver

class User(AbstractUser):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

@receiver(pre_save, sender=User)
def force_username_email_parity(sender, instance, **kwargs):
    """
    Force the username to be the same as email for auth purposes.
    """
    instance.username = instance.email
