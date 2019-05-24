from rest_framework import serializers

from contests.models import Contest


class ContestSerializer(serializers.HyperlinkedModelSerializer):
    host_country = serializers.PrimaryKeyRelatedField(queryset=Contest.objects.all())

    class Meta:
        model = Contest
        fields = '__all__'
        depth = 1
