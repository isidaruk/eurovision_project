# from .celery import app as celery_app
from __future__ import absolute_import, unicode_literals

from celery import shared_task

from django.db.models import Sum
from django.apps import apps

from participants.models import Participant


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


# @shared_task
# def count_votes():
#     return Vote.objects.count()


@shared_task
def recalculate_total_votes_for_participant(to_participant_id):
    # from votes.models import Vote
    # from django.apps import apps
    Vote = apps.get_model('votes.Vote')
    total = Vote.objects.filter(to_participant=to_participant_id).aggregate(Sum('point'))
    total_score = total['point__sum']

    participant = Participant.objects.get(id=to_participant_id)
    participant.total_score = total_score
    participant.save()

    return total_score
