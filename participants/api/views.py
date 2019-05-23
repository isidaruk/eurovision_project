from rest_framework import viewsets

from participants.models import Participant
from participants.api.serializers import ParticipantSerializer


class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer