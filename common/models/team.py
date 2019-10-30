from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .base import BaseModel
from .user import User

class Team(BaseModel):
    name    = models.CharField(_('name'), max_length=255)
    users   = models.ManyToManyField(User, blank=True, related_name='teams')

    def __str__(self):
        return f'{self.name} ({str(self.id)[-5:]})'

@receiver(post_save, sender=User)
def create_team_on_user_creation(sender, instance, **kwargs):
    """Create a team for the user when a user is created"""
    if kwargs.get('created', False):
        team = Team.objects.create(name=f"{instance.email}'s Team")
        team.users.add(instance)
