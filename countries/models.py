from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=56, unique=True)

    class Meta:
        verbose_name = 'country'
        verbose_name_plural = 'countries'

    def __str__(self):
        return self.name
