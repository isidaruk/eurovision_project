# -*-  -*-
# Automated test of the api
import pytest

import json

from .factories import (
    ArtistFactory,
    CountryFactory,
    ContestFactory,
    ParticipantFactory,
    VoterFactory,
    VoteFactory,
)


# # 1
# # test countries response get's a 200 code:
# @pytest.mark.django_db  # -- This is a helper and it is necessary to mark a that this test function is requiring the database.
# def test_countries_endpoint(client):
#     new_country = CountryFactory()
#     response = client.get(f'/api/v0/countries/{new_country.id}', follow=True)
#     assert response.status_code == 200


# # 2
# # test contests response get's a 200 code, and the host_coountry and the year api returned is the we actually want:
# @pytest.mark.django_db
# def test_contests_endpoint(client):
#     new_contest = ContestFactory()
#     response = client.get(f'/api/v0/contests/{new_contest.id}', follow=True)
#     content = json.loads(response.content)
#     assert response.status_code == 200
#     assert content['host_country'] == new_contest.host_country.id
#     assert content['year'] == new_contest.year


# 3
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


@pytest.fixture
def votes(voters, participants):

    vts = []
    for p in participants:
        vts.append(VoteFactory(from_voter=voters[0], to_participant=p))

    return vts


@pytest.mark.django_db
def test_participants_and_voters(participants, voters, votes):
    for p in participants:
        print('PARTICIPANT:', p)

    for v in voters:
        print('VOTER:', v)

    for vt in votes:
        print('VOTE:', vt)

    assert len(participants) == 12
    assert len(voters) == 12
    assert len(votes) == 12
