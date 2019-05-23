from django.db import models

from artists.models import Artist
from contests.models import Contest
from countries.models import Country


class Participant(models.Model):
    artist_id = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
    )
    country_id = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
    )

    song = models.CharField(max_length=200)

    contest_id = models.ForeignKey(
        Contest,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'participant'
        verbose_name_plural = 'participants'

    def __str__(self):
        return '{} - {} - {} - Eurovision {}'.format(
            self.artist_id.name, self.song, self.country_id.name, self.contest_id.year
        )
