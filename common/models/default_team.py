import logging

from django.db import models, IntegrityError
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .base import BaseModel
from .team import Team
from .user import User

logger = logging.getLogger(__name__)

class DefaultTeam(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='default_team')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def clean(self):
        # Check that user belongs to the team
        if not self.team.users.filter(id=self.user.id).exists():
            raise ValidationError(f"User {self.user} doesn't belong to team {self.team}")

def set_default_team_if_not_set(sender, instance, action, **kwargs):
    """Set the default team for each team user if it doesn't already exist.

    This fires every time a Team-User many-to-many relationship is changed
    (added/removed).This could lead to inefficiencies in the future when teams
    grow large, but for now it's great for integrity.
    """
    for user in instance.users.all():
        try:
            DefaultTeam.objects.create(user=user, team=instance)
        except IntegrityError:
            logger.info(f"Can't set default team for user {user}, it already exists.")
m2m_changed.connect(set_default_team_if_not_set, sender=Team.users.through)
