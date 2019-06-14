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
    return ContestFactory(host_country=country)


@pytest.fixture
def participants(artists, countries, contest):

    participants = []
    for a, c in zip(artists, countries):
        participants.append(ParticipantFactory(artist=a, country=c, contest=contest))

    return participants


@pytest.fixture
def voters(countries, contest):

    voters = []
    for c in countries:
        voters.append(VoterFactory(country=c, contest=contest))

    return voters


@pytest.mark.django_db
def test_vote_post_endpoint_data(voters, participants):
    endpoint = 'http://127.0.0.1:8000/api/v0/votes/'
    from_voter = voters[0].id  # from voter from Country 0
    to_participant = participants[1].id  # to participant from Country 1
    point = 12
    token = str(voters[0].vote_key)
    # token = '00000000-0000-0000-0000-000000000000'
    token = 'a3a805aa-ca20-41da-8c9b-85547990b79f'  # -- token for id 1 - Belarus
    status_code = 200

    print(from_voter, to_participant, point, token)

    resp = requests.post(endpoint, data=json.dumps({
        "from_voter": from_voter,
        "to_participant": to_participant,
        "point": point
    }), headers={"Content-Type": "application/json", "Token": token})

    print(resp.content)
    assert resp.status_code == status_code
