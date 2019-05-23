from rest_framework import viewsets

from countries.api.serializers import CountrySerializer
from countries.models import Country


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
