from rest_framework import serializers

from participants.models import Participant

from artists.models import Artist
from contests.models import Contest
from countries.models import Country


# class ParticipantSerializer(serializers.HyperlinkedModelSerializer):
class ParticipantSerializer(serializers.ModelSerializer):
    artist = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all())
    contest = serializers.PrimaryKeyRelatedField(queryset=Contest.objects.all())
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())

    total_score = serializers.ReadOnlyField()

    class Meta:
        model = Participant
        fields = '__all__'

        depth = 1
