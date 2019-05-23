from rest_framework import viewsets

from votes.models import Vote
from votes.api.serializers import VoteSerializer


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
