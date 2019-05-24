from rest_framework import serializers

from participants.models import Participant

from artists.api.serializers import ArtistSerializer
from contests.api.serializers import ContestSerializer
from countries.api.serializers import CountrySerializer


class ParticipantSerializer(serializers.HyperlinkedModelSerializer):
    artist = ArtistSerializer
    contest = ContestSerializer
    country = CountrySerializer

    class Meta:
        model = Participant
        fields = '__all__'

        depth = 1
