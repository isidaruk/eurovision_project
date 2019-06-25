from django.core.validators import MaxValueValidator
from django.db import models, transaction

from participants.models import Participant
from voters.models import Voter
from votes.tasks import (
    recalculate_total_votes_for_participant,
)

# A total of 1.160 points (1, 2, 3, 4, 5, 6, 7, 8, 10, 12 points x 20 participating countries).
POINT_CHOICES = [
    (1, '1 Point'),
    (2, '2 Points'),
    (3, '3 Points'),
    (4, '4 Points'),
    (5, '5 Points'),
    (6, '6 Points'),
    (7, '7 Points'),
    (8, '8 Points'),
    (10, '10 Points'),
    (12, '12 Points'),
]


class Vote(models.Model):
    point = models.PositiveIntegerField(choices=POINT_CHOICES, default=1, validators=[MaxValueValidator(12)])

    from_voter = models.ForeignKey(Voter, on_delete=models.CASCADE, default=None)
    to_participant = models.ForeignKey(Participant, on_delete=models.CASCADE,)

    def save(self, *args, **kwags):
        super(Vote, self).save(*args, **kwags)

        transaction.on_commit(lambda: recalculate_total_votes_for_participant.delay(self.to_participant.id))

    def __str__(self):
        return '{} points from {} ({}) to {} - {}'.format(
            self.point,
            self.from_voter.country,
            self.from_voter.vote_key,
            self.to_participant.artist.name,
            self.to_participant.country.name
        )
