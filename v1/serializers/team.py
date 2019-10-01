from rest_framework import serializers

from common.models import Team

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Team
        fields  = '__all__'
