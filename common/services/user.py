from django.contrib.auth import get_user_model

from common.models import Team

User = get_user_model()

def get_teams_from_user(user):
    """Gets all teams which the user belongs to

    Args:
    - user (User): The user in question

    Returns:
    - Queryset (Team): A queryset of Team objects
    """
    return Team.objects.filter(users__id=user.id)
