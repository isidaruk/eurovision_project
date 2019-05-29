from rest_framework import serializers

from votes.models import Vote
from voters.models import Voter
from participants.models import Participant


# class VoteSerializer(serializers.HyperlinkedModelSerializer):
class VoteSerializer(serializers.ModelSerializer):
    from_voter = serializers.PrimaryKeyRelatedField(queryset=Voter.objects.all())
    to_participant = serializers.PrimaryKeyRelatedField(queryset=Participant.objects.all())

    class Meta:
        model = Vote
        fields = '__all__'
        depth = 1
