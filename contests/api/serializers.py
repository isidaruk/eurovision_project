from rest_framework import serializers

from contests.models import Contest
from countries.models import Country


class ContestSerializer(serializers.HyperlinkedModelSerializer):
    host_country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all())

    class Meta:
        model = Contest
        fields = '__all__'
        depth = 1
