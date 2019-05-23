from rest_framework import viewsets

from artists.models import Artist
from artists.api.serializers import ArtistSerializer


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
