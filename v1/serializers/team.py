from django.contrib.auth import get_user_model
from rest_framework import serializers

from common.models import Team

User = get_user_model()

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model               = Team
        fields              = '__all__'
        read_only_fields    = ('users',)

class TeamDetailSerializer(TeamSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
