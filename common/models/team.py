from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel, AppUser

class Team(BaseModel, models.Model):
    name    = models.CharField(_('name'), max_length=255)
    users   = models.ManyToManyField(AppUser)

    def __str__(self):
        return f'{self.name} ({str(self.id)[-5:]})'
