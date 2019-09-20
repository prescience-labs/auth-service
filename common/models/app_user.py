from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel

class AppUser(BaseModel, models.Model):
    provider_id = models.CharField(max_length=1000, help_text=_('ID associated with our auth provider'))
