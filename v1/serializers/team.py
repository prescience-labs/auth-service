from django.contrib.auth import get_user_model
from rest_framework import serializers

from common.models import Team

User = get_user_model()

class TeamSerializer(serializers.ModelSerializer):
    users = serializers.HiddenField(default=None)

    class Meta:
        model   = Team
        fields  = '__all__'

class TeamDetailSerializer(TeamSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
