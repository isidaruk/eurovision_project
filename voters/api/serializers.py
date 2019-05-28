from rest_framework import serializers

from voters.models import Voter


class VoterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Voter
        fields = '__all__'
        # depth = 1
