from django.db import models

from countries.models import Country


class Contest(models.Model):
    year = models.IntegerField(unique=True)
    host_country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='contests',
        related_query_name='eurovision',
    )

    class Meta:
        verbose_name = 'contest'
        verbose_name_plural = 'contests'

    def __str__(self):
        return 'Eurovision {}'.format(self.year)
