import logging

from django.db import models, IntegrityError
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .base import BaseModel
from .team import Team
from .user import User

logger = logging.getLogger(__name__)

class DefaultTeam(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def clean(self):
        # Check that user belongs to the team
        if not self.team.users.filter(id=self.user.id).exists():
            raise ValidationError(f"User {self.user} doesn't belong to team {self.team}")

@receiver(pre_save, sender=Team)
def set_default_team_if_not_set(sender, instance, **kwargs):
    """Set the default team for each team user if it doesn't already exist."""
    for user in instance.users.all():
        try:
            DefaultTeam.objects.create(user=user, team=instance)
        except IntegrityError:
            logger.info(f"Can't set default team for user {user}, it already exists.")
