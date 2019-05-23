from django.db import models

from countries.models import Country


class Vote(models.Model):
    point = models.PositiveIntegerField(default=0)

    from_country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='from_votes',
    )
    to_country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='to_votes',
    )
