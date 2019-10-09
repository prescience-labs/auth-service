from rest_framework import generics

from common.models import Team
from v1.serializers import TeamSerializer, TeamDetailSerializer

class TeamList(generics.ListCreateAPIView):
    queryset            = Team.objects.all()
    serializer_class    = TeamSerializer

class TeamDetail(generics.RetrieveUpdateAPIView):
    queryset            = Team.objects.all()
    serializer_class    = TeamDetailSerializer
