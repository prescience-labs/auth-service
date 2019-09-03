import uuid

# from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models.signals import pre_save
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .user import User

class Team(models.Model):
    uid     = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name    = models.CharField(_('name'), max_length=255)
    users   = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.name} ({self.uid})'
