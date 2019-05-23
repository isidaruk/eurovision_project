from rest_framework import serializers

from participants.models import Participant

from contests.models import Contest
from countries.models import Country

from artists.api.serializers import ArtistSerializer
# from contests.api.serializers import ContestSerializer
# from countries.api.serializers import CountrySerializer


class ContestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contest
        fields = '__all__'
        # fields = ('year', 'host_country',)


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'
        # fields = ('name',)


class ParticipantSerializer(serializers.ModelSerializer):
    # artist_id = ArtistSerializer(many=True)
    # contest_id = ContestSerializer(many=True)
    # country_id = CountrySerializer(many=True)

    artist_id = ArtistSerializer
    contest_id = ContestSerializer
    country_id = CountrySerializer

    class Meta:
        model = Participant
        fields = '__all__'
