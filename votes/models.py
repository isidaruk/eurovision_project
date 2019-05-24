from django.db import models
from django.core.validators import MaxValueValidator

from countries.models import Country
from participants.models import Participant


class Vote(models.Model):
    point = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(12)], unique=True)

    from_country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='from_votes',
    )
    to_country = models.ForeignKey(
        Participant,
        on_delete=models.CASCADE,
        related_name='to_votes',
    )

    def __str__(self):
        return '{} points from {} to {} ({})'.format(
            self.point, self.from_country.name, self.to_country.artist_id.name, self.to_country.country_id.name
        )
