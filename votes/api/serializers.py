from rest_framework import serializers

from participants.models import Participant
from voters.models import Voter
from votes.models import Vote


class VoteSerializer(serializers.ModelSerializer):
    from_voter = serializers.PrimaryKeyRelatedField(queryset=Voter.objects.all())
    to_participant = serializers.PrimaryKeyRelatedField(queryset=Participant.objects.all())

    class Meta:
        model = Vote
        fields = '__all__'
        depth = 1
