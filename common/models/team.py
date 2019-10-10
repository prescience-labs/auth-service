from django.db import models
from django.utils.translation import gettext_lazy as _

from .base import BaseModel
from .user import User

class Team(BaseModel):
    name    = models.CharField(_('name'), max_length=255)
    users   = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f'{self.name} ({str(self.id)[-5:]})'
