from __future__ import absolute_import, unicode_literals

from django.apps import apps
from django.db.models import Sum
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from celery import shared_task

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@shared_task
def recalculate_total_votes_for_participant(to_participant_id):
    Vote = apps.get_model('votes.Vote')
    total = Vote.objects.filter(to_participant=to_participant_id).aggregate(Sum('point'))
    total_score = total['point__sum']

    cache.set(to_participant_id, total_score, CACHE_TTL)
    print(f'Score for participant {to_participant_id}: {total_score}. Caching...')

    return total_score
