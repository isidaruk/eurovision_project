from rest_framework import serializers

from participants.models import Participant

from artists.models import Artist
from contests.models import Contest
from countries.models import Country

from django.core.cache import cache


# class ParticipantSerializer(serializers.HyperlinkedModelSerializer):
class ParticipantSerializer(serializers.ModelSerializer):
    artist = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all())
    contest = serializers.PrimaryKeyRelatedField(queryset=Contest.objects.all())
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())

    # total_score = serializers.ReadOnlyField()
    total_score = serializers.SerializerMethodField()

    class Meta:
        model = Participant
        fields = '__all__'

        depth = 1

    def get_total_score(self, obj):

        # Get total score for this Participant from cache, or recalculate it.
        total_score_cached = cache.get(obj.pk, default=None)

        if total_score_cached is None:
            total_score_data = obj.total_score
            cache.set(pk, total_score_data, CACHE_TTL)
            print(f'Score for participant {pk}: {total_score_data}. Caching...')
            return total_score_data

        return total_score_cached
