from django.core.exceptions import PermissionDenied
from django.http import (
    HttpResponseBadRequest,
    HttpResponseForbidden,
)

from participants.models import Participant
from voters.models import Voter
from votes.models import Vote


def check_token(token, from_voter):
    return str(token) == str(Voter.objects.get(id=from_voter).vote_key)


def check_voters(validated_data):
    errors = []

    vote_point = validated_data.get('point')
    from_voter = validated_data.get('from_voter')
    to_participant = validated_data.get('to_participant')

    voter = Voter.objects.get(id=from_voter.id)
    participant = Participant.objects.get(id=to_participant.id)

    # Count how many times voter has voted.
    if Vote.objects.filter(from_voter=from_voter.id).count() >= 10:
        errors.append("You've voted 10 times.")
    else:

        # If the point is not used.
        if Vote.objects.filter(from_voter=from_voter.id).filter(point__iexact=vote_point).count() != 0:
            errors.append(f"{vote_point} point is already given.")

        # Voting for your own country.
        if voter.country.name == participant.country.name:
            errors.append('You are not allowed to vote for your own country.')

        # Check vote for the same country.
        if Vote.objects.filter(to_participant=to_participant.id).exists():
            errors.append("You've already given a point to these participant.")

    data = (vote_point, voter.country.name, participant.country.name)

    return errors, data
