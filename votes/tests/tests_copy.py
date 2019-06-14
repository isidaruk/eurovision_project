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


# 12 countries for participants, including host_country and country that are not the participant of tested contest
@pytest.fixture
def artists():
    return ArtistFactory.create_batch(9)


@pytest.fixture
def countries():
    return CountryFactory.create_batch(9)


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


# @pytest.mark.django_db
# def test_vote_post_endpoint_data(client, voters, participants):

#     v = voters[1]

#     p = participants[2]

#     print(len(Voter.objects.all()))
#     print(len(Participant.objects.all()))

#     print(v)
#     print(p)

#     from_voter = v.id
#     to_participant = p.id
#     point = 12
#     token = v.vote_key

#     status_code = 201  # if created

#     print('Test data:', v.country.name, '||', p.country.name, '||', point, '||', token)

#     resp = client.post('/api/v0/votes/',
#                        {
#                            "from_voter": from_voter,
#                            "to_participant": to_participant,
#                            "point": point
#                        },
#                        HTTP_TOKEN=f'{token}')

#     data = {
#         "id": 1,
#         "from_voter": from_voter,
#         "to_participant": to_participant,
#         "point": point
#     }

#     content = json.loads(resp.content)
#     print(content)

#     assert resp.status_code == status_code
#     assert content == data


# test case with 10 votes
@pytest.fixture
def votes(voters, participants):

    # vts = []
    # for p in participants:
    #     vts.append(VoteFactory(from_voter=voters[0], to_participant=p))

    # return vts

    return [VoteFactory(from_voter=voters[0], to_participant=p) for p in participants]


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

    v = voters[0]

    # trying to vote for 10th and 11th
    p_10 = two_more_participants[0]
    p_11 = two_more_participants[1]

    print(len(Voter.objects.all()))
    print(len(Participant.objects.all()))

    print(v)
    print(p_10)
    print(p_11)

    from_voter = v.id
    to_participant = p_10.id
    point = 12
    token = v.vote_key

    status_code = 201  # if created

    print('Test data:', v.country.name, '||', p_10.country.name, '||', point, '||', token)

    resp = client.post('/api/v0/votes/',
                       {
                           "from_voter": from_voter,
                           "to_participant": to_participant,
                           "point": point
                       },
                       HTTP_TOKEN=f'{token}')

    data = {
        "id": 10,
        "from_voter": from_voter,
        "to_participant": to_participant,
        "point": point
    }

    content = json.loads(resp.content)
    print(content)

    assert resp.status_code == status_code
    assert content == data

    # not allowed case
    status_code2 = 400  # if created
    resp2 = client.post('/api/v0/votes/',
                        {
                            "from_voter": from_voter,
                            "to_participant": p_11.id,
                            "point": point
                        },
                        HTTP_TOKEN=f'{token}')

    data2 = ["You've voted 10 times."]

    content2 = json.loads(resp2.content)
    print(content2)

    assert resp2.status_code == status_code2
    assert content2 == data2
