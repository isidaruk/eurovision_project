import json
import pytest

import requests

from .factories import (
    ArtistFactory,
    CountryFactory,
    ContestFactory,
    ParticipantFactory,
    VoterFactory,
    VoteFactory,
)

from voters.models import Voter
from participants.models import Participant


@pytest.fixture
def artists():
    return ArtistFactory.create_batch(9)


@pytest.fixture
def countries():
    return CountryFactory.create_batch(9)


@pytest.fixture
def contest():
    country = CountryFactory()
    return ContestFactory.create(host_country=country)


@pytest.fixture
def participants(artists, countries, contest):
    return [ParticipantFactory.create(artist=a, country=c, contest=contest) for a, c in zip(artists, countries)]


@pytest.fixture
def voters(countries, contest):
    return [VoterFactory.create(country=c, contest=contest) for c in countries]


# Create 9 votes in db.
@pytest.fixture
def votes(voters, participants):
    return [VoteFactory(from_voter=voters[0], to_participant=p) for p in participants]

# Create 2 more participants in addition to exising 9.


@pytest.fixture
def two_more_participants(contest):
    artist10 = ArtistFactory()
    artist11 = ArtistFactory()

    country10 = CountryFactory()
    country11 = CountryFactory()

    p_10 = ParticipantFactory.create(artist=artist10, country=country10, contest=contest)
    p_11 = ParticipantFactory.create(artist=artist11, country=country11, contest=contest)

    return [p_10, p_11]


@pytest.mark.django_db
def test_vote_post_cases(client, voters, participants, votes, two_more_participants):

    # The same voter for all cases - Country 0.
    v = voters[0]
    # print(v)

    # Test vote 10th and 11th time.
    p_10 = two_more_participants[0]
    p_11 = two_more_participants[1]
    # print(p_10)
    # print(p_11)

    # print(len(Voter.objects.all()))
    # print(len(Participant.objects.all()))

    from_voter = v.id
    to_participant10 = p_10.id
    to_participant11 = p_11.id
    point = 12
    token = v.vote_key

    status_code = 201  # if created
    status_code2 = 400

    print('Test data:', v.country.name, '||', p_10.country.name, '||', point, '||', token)

    resp = client.post('/api/v0/votes/',
                       {
                           "from_voter": from_voter,
                           "to_participant": to_participant10,
                           "point": point
                       },
                       HTTP_TOKEN=f'{token}')

    data = {
        "id": 10,
        "from_voter": from_voter,
        "to_participant": to_participant10,
        "point": point
    }

    resp2 = client.post('/api/v0/votes/',
                        {
                            "from_voter": from_voter,
                            "to_participant": to_participant11,
                            "point": point
                        },
                        HTTP_TOKEN=f'{token}')

    data2 = ["You've voted 10 times."]

    content = json.loads(resp.content)
    # print(content)

    assert resp.status_code == status_code
    assert content == data

    content2 = json.loads(resp2.content)
    # print(content2)

    assert resp2.status_code == status_code2
    assert content2 == data2
