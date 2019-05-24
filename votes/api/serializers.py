from rest_framework import serializers

from votes.models import Vote
from countries.models import Country
from participants.models import Participant


class VoteSerializer(serializers.HyperlinkedModelSerializer):
    from_country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())
    to_country = serializers.PrimaryKeyRelatedField(queryset=Participant.objects.all())

    class Meta:
        model = Vote
        fields = '__all__'
        depth = 1
