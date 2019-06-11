from django.apps import apps

from django.db import models

from artists.models import Artist
from contests.models import Contest
from countries.models import Country


class Participant(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE,)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='participants')

    song = models.CharField(max_length=200)

    contest = models.ForeignKey(Contest, on_delete=models.CASCADE, related_name='participants')

    # total_score = models.PositiveIntegerField(default=0)

    @property
    def total_score(self):
        Vote = apps.get_model('votes.Vote')

        return Vote.objects.filter(to_participant=self.id).aggregate(models.Sum('point'))['point__sum']

    class Meta:
        verbose_name = 'participant'
        verbose_name_plural = 'participants'

    def __str__(self):
        return '{} - {} - {} - Eurovision {}'.format(
            self.artist.name, self.song, self.country.name, self.contest.year
        )
