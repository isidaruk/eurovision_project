from django.db import models
from django.core.validators import MaxValueValidator

from countries.models import Country
from participants.models import Participant


class Vote(models.Model):
    point = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(12)], unique=True)

    from_country = models.ForeignKey(Country, on_delete=models.CASCADE,)
    to_country = models.ForeignKey(Participant, on_delete=models.CASCADE,)

    def __str__(self):
        return '{} points from {} to {} ({})'.format(
            self.point, self.from_country.name, self.to_country.artist.name, self.to_country.country.name
        )
