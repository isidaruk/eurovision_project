from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest, HttpResponseForbidden
from votes.models import Vote
from voters.models import Voter
from participants.models import Participant


def check_token(token, from_voter):
    # if token:
    #
    #     # If voter have Token.
    #     if from_voter and sended_vote_key:
    #
    #         if str(from_voter.vote_key) != str(sended_vote_key):
    #             # return HttpResponseForbidden(content='You are not allowed to vote this year.')
    #             errors.append('You are not allowed to vote this year.')
    # pass
    return str(token) == str(Voter.objects.get(id=from_voter).vote_key)

    # return bool(Voter.objects.get(id=from_voter)) if (token and from_voter) else False


def check_voters(validated_data):
    errors = []

    vote_point = validated_data.get('point')
    from_voter = validated_data.get('from_voter')
    to_participant = validated_data.get('to_participant')

    voter = Voter.objects.get(id=from_voter.id)
    participant = Participant.objects.get(id=to_participant.id)

    # -*- Check Cases -*-

    # Count how many times voter has voted.
    if Vote.objects.filter(from_voter=from_voter.id).count() >= 10:
        # raise PermissionDenied()
        # return HttpResponseBadRequest(content="You've voted 10 times.")
        errors.append("You've voted 10 times.")
    else:

        # If the point is not used.
        if Vote.objects.filter(from_voter=from_voter.id).filter(point__iexact=vote_point).count() != 0:  # ?
            # return HttpResponseBadRequest(content=f"{vote_point} point is already given.")
            errors.append(f"{vote_point} point is already given.")

        # Voting for your own country.
        if voter.country.name == participant.country.name:
            # return HttpResponseBadRequest(content='You are not allowed to vote for your own country.')
            errors.append('You are not allowed to vote for your own country.')

        # Check vote for the same country.
        if Vote.objects.filter(to_participant=to_participant.id).exists():
            # return HttpResponseBadRequest(content="You've already given a point to these participant.")
            errors.append("You've already given a point to these participant.")

    return errors
