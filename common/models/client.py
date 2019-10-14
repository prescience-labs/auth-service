from uuid import uuid4

from django.contrib.auth.models import Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

from .base import BaseModel
from .user import User

class Client(BaseModel):
    name            = models.CharField(_('name'), max_length=255)
    client_id       = models.CharField(_('client ID'), max_length=255, default=uuid4(), unique=True, help_text=_('We use a different ID than the object ID to preserve database security'))
    client_secret   = models.CharField(_('client secret'), max_length=255, default=uuid4(), unique=True)
    permissions     = models.ManyToManyField(Permission)

    def __str__(self):
        return f'{self.name} ({str(self.id)[-5:]})'
