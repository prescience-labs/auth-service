from django.contrib.auth import get_user_model
from rest_framework import serializers

from common.models import Team
from .team import TeamSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    teams = serializers.HiddenField(default=None)

    class Meta:
        model   = User
        fields  = [
            'id',
            'email',
            'is_active',
            'teams',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'is_active',
            'created_at',
            'updated_at',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

class UserDetailSerializer(UserSerializer):
    teams = serializers.SerializerMethodField('get_teams')

    def get_teams(self, obj):
        """Forces the `teams` field to return a list of IDs"""
        teams_queryset = Team.objects.filter(users__id=obj.id)
        return [t.id for t in teams_queryset]
