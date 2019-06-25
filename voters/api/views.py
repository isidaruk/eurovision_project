from rest_framework import viewsets

from voters.api.serializers import VoterSerializer
from voters.models import Voter


class VoterViewSet(viewsets.ModelViewSet):
    queryset = Voter.objects.all()
    serializer_class = VoterSerializer
