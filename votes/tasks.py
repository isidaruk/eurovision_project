from __future__ import absolute_import, unicode_literals

from celery import shared_task

from django.db.models import Sum
from django.apps import apps


@shared_task
def recalculate_total_votes_for_participant(to_participant_id):
    Vote = apps.get_model('votes.Vote')
    total = Vote.objects.filter(to_participant=to_participant_id).aggregate(Sum('point'))
    total_score = total['point__sum']

    return total_score
