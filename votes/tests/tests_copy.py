import json
import pytest

import requests

from .factories import (
    ArtistFactory,
    CountryFactory,
    ContestFactory,
    ParticipantFactory,
    VoterFactory,
    # VoteFactory,
)


# 12 countries for participants, including host_country and country that are not the participant of tested contest
@pytest.fixture
def artists():
    return ArtistFactory.create_batch(12)


@pytest.fixture
def countries():
    return CountryFactory.create_batch(12)


# instance of the contest to use
@pytest.fixture
def contest():
    country = CountryFactory()
    return ContestFactory.create(host_country=country)


@pytest.fixture
def participants(artists, countries, contest):

    # participants = []
    # for a, c in zip(artists, countries):
    #     participants.append(ParticipantFactory(artist=a, country=c, contest=contest))

    # return participants

    return [ParticipantFactory.create(artist=a, country=c, contest=contest) for a, c in zip(artists, countries)]


@pytest.fixture
def voters(countries, contest):

    # voters = []
    # for c in countries:
    #     voters.append(VoterFactory(country=c, contest=contest))

    # return voters

    return [VoterFactory.create(country=c, contest=contest) for c in countries]


# ####
from voters.models import Voter
from participants.models import Participant


@pytest.mark.django_db
def test_vote_post_endpoint_data(voters, participants):
    endpoint = 'http://127.0.0.1:8000/api/v0/votes/'

    # #### take data created from fixtures
    print('COUNT', Voter.objects.count())

    for v in Voter.objects.all():
        print('VOTER ID', v.id)

    from_voter = Voter.objects.get(id=1).id
    to_participant = Participant.objects.get(id=2).id
    point = 12
    token = str(voters[0].vote_key)
    status_code = 200
    # token = '00000000-0000-0000-0000-000000000000'
    token = 'a3a805aa-ca20-41da-8c9b-85547990b79f'

# ####
#     from_voter = voters[0].id  # from voter from Country 0
#     to_participant = participants[1].id  # to participant from Country 1
#     point = 12
#     token = str(voters[0].vote_key)
#     # token = '00000000-0000-0000-0000-000000000000'
#     token = 'a3a805aa-ca20-41da-8c9b-85547990b79f'  # -- token for id 1 - Belarus
#     status_code = 200
# ####

    print(from_voter, to_participant, point, token)

    resp = requests.post(endpoint, data=json.dumps({
        "from_voter": from_voter,
        "to_participant": to_participant,
        "point": point
    }), headers={"Content-Type": "application/json", "Token": token})

    print(resp.content)
    assert resp.status_code == status_code


# # #### Test that objects are created in db
# from voters.models import Voter
# from participants.models import Participant


# @pytest.mark.django_db
# def test_voters_count(voters):
#     for v in Voter.objects.all():
#         print(v)

#     assert Voter.objects.count() == 12  # 4 + 12 if with data created manually


# @pytest.mark.django_db
# def test_participants_count(participants):
#     for p in Participant.objects.all():
#         print(p)

#     assert Participant.objects.count() == 12  # 7 + 12 if with data created manually
