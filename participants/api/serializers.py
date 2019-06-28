from django.core.cache import cache

from rest_framework import serializers

from artists.models import Artist
from contests.models import Contest
from countries.models import Country
from participants.models import Participant

from eurovision_project.settings import CACHES


class ParticipantSerializer(serializers.ModelSerializer):
    artist = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all())
    contest = serializers.PrimaryKeyRelatedField(queryset=Contest.objects.all())
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())

    total_score = serializers.SerializerMethodField()

    class Meta:
        model = Participant
        fields = '__all__'
        depth = 1

    def get_total_score(self, obj):
        """Get total score for this Participant from cache, or return None."""

        prefix = CACHES['default']['APPS_KEY_PREFIX']['participants']
        return cache.get(f'{prefix}.{obj.pk}', default=None)
