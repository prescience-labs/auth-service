import logging

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from rest_framework import serializers

from common.models import Team
from .team import TeamSerializer

logger  = logging.getLogger(__name__)
User    = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    team    = serializers.UUIDField(required=False, default=None)
    teams   = serializers.SerializerMethodField('get_teams')

    def get_teams(self, obj):
        """Forces the `teams` field to return a list of IDs"""
        teams_queryset = Team.objects.filter(users__id=obj.id)
        return [t.id for t in teams_queryset]

    class Meta:
        model   = User
        fields  = [
            'id',
            'email',
            'password',
            'is_active',
            'team',
            'teams',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'is_active',
            'teams',
            'created_at',
            'updated_at',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['email'],
            password=validated_data['password'],
        )

        # Attempt to add the user to the team.
        # If no team was listed, or if the user couldn't be added to the team,
        # create a new team for the user.
        try:
            team = Team.objects.get(pk=validated_data['team'])
        except:
            logger.info(f"User couldn't be added to the given team or no team was given. Creating a new team...")
            team = Team.objects.create(name=f"{user.email}'s Team")

        team.users.add(user)
        return user

class UserDetailSerializer(UserSerializer):
    teams = serializers.SerializerMethodField('get_teams')

    def get_teams(self, obj):
        """Forces the `teams` field to return a list of IDs"""
        teams_queryset = Team.objects.filter(users__id=obj.id)
        return [t.id for t in teams_queryset]
