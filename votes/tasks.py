from __future__ import absolute_import, unicode_literals

import logging

from django.apps import apps
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.db.models import Sum

from celery import shared_task

from eurovision_project.settings import CACHES

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

logger = logging.getLogger('vote')


@shared_task
def recalculate_total_votes_for_participant(to_participant_id):
    Vote = apps.get_model('votes.Vote')
    total = Vote.objects.filter(to_participant=to_participant_id).aggregate(Sum('point'))
    total_score = total['point__sum']

    prefix = CACHES['default']['APPS_KEY_PREFIX']['participants']
    cache.set(f'{prefix}.{to_participant_id}', total_score, CACHE_TTL)
    logger.info(f'Score for participant {to_participant_id}: {total_score}. Caching...')

    return total_score
