from rest_framework import viewsets

from voters.models import Voter
from voters.api.serializers import VoterSerializer


class VoterViewSet(viewsets.ModelViewSet):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
