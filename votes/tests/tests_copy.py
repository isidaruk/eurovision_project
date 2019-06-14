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

from voters.models import Voter
from participants.models import Participant


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


@pytest.mark.django_db
def test_vote_post_endpoint_data(client, voters, participants):

    v = voters[1]

    p = participants[2]

    print(len(Voter.objects.all()))
    print(len(Participant.objects.all()))

    print(v)
    print(p)

    from_voter = v.id
    to_participant = p.id
    point = 12
    token = v.vote_key

    status_code = 201  # if created

    print('Test data:', v.country.name, '||', p.country.name, '||', point, '||', token)

    resp = client.post('/api/v0/votes/',
                       {
                           "from_voter": from_voter,
                           "to_participant": to_participant,
                           "point": point
                       },
                       HTTP_TOKEN=f'{token}')

    data = {
        "id": 1,
        "from_voter": from_voter,
        "to_participant": to_participant,
        "point": point
    }

    content = json.loads(resp.content)
    print(content)

    assert resp.status_code == status_code
    assert content == data
