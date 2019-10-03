from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel

class AppUser(BaseModel):
    """Tracks users in Django by the id for the provider (e.g. Auth0)"""
    provider_id = models.CharField(max_length=1000, help_text=_('ID associated with our auth provider'))
