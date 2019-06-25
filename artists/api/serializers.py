from rest_framework import serializers

from artists.models import Artist


class ArtistSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Artist
        fields = '__all__'
