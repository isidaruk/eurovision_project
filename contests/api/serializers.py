from rest_framework import serializers

from contests.models import Contest


class ContestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contest
        fields = '__all__'
        depth = 1
