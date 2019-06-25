from rest_framework import viewsets

from artists.api.serializers import ArtistSerializer
from artists.models import Artist


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
