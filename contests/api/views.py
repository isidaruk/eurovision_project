from rest_framework import viewsets

from contests.models import Contest
from contests.api.serializers import ContestSerializer


class ContestViewSet(viewsets.ModelViewSet):
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer
