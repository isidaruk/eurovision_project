from django.db import models

from contests.models import Contest
from countries.models import Country

import uuid


class Voter(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    vote_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return 'Voter from {}, Eurovision {}'.format(self.country.name, self.contest.year)
