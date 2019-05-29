from django.db import models
from django.core.validators import MaxValueValidator

from participants.models import Participant
from voters.models import Voter


class Vote(models.Model):
    point = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(12)], unique=True)

    from_voter = models.ForeignKey(Voter, on_delete=models.CASCADE, default=None)
    to_participant = models.ForeignKey(Participant, on_delete=models.CASCADE,)

    def __str__(self):
        return '{} points from {} ({}) to {} - {}'.format(
            self.point, self.from_voter.country, self.from_voter.vote_key, self.to_participant.artist.name, self.to_participant.country.name
        )
