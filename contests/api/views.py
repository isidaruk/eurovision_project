from rest_framework import viewsets

from contests.api.serializers import ContestSerializer
from contests.models import Contest


class ContestViewSet(viewsets.ModelViewSet):
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer
