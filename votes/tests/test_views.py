import json

import pytest

from votes.models import Vote

from .factories import (
    ArtistFactory,
    ContestFactory,
    CountryFactory,
    ParticipantFactory,
    VoteFactory,
    VoterFactory,
)


@pytest.fixture
def contest():
    return ContestFactory(year=2019, host_country=CountryFactory(name='Israel'))


@pytest.fixture
def country_rus():
    return CountryFactory(name='Russia')


@pytest.fixture
def voter_rus(contest, country_rus):
    return VoterFactory(country=country_rus, contest=contest)


@pytest.fixture
def participant_bel(contest):
    return ParticipantFactory(artist=ArtistFactory(), country=CountryFactory(name='Belarus'), contest=contest)


@pytest.mark.django_db
def test_vote_created(client, contest, participant_bel, voter_rus):
    from_voter = voter_rus.id
    to_participant = participant_bel.id
    point = 12
    token = voter_rus.vote_key

    status_code = 201
    data = {
        "id": 1,
        "from_voter": from_voter,
        "to_participant": to_participant,
        "point": point
    }

    resp = client.post('/api/v0/votes/',
                       {
                           "from_voter": from_voter,
                           "to_participant": to_participant,
                           "point": point
                       },
                       HTTP_TOKEN=f'{token}')

    content = json.loads(resp.content)

    assert resp.status_code == status_code
    assert content == data


@pytest.mark.django_db
def test_vote_with_invalid_token(client, participant_bel, voter_rus):
    resp = client.post('/api/v0/votes/',
                       {
                           "from_voter": voter_rus.id,
                           "to_participant": participant_bel.id,
                           "point": 12
                       },
                       HTTP_TOKEN=f'{voter_rus.vote_key}' + 'X')

    status_code = 403
    data = "You do not have permission to perform this action."

    content = json.loads(resp.content)

    assert resp.status_code == status_code
    assert content['detail'] == data


@pytest.mark.django_db
def test_vote_for_own_country(client, contest, country_rus, voter_rus):
    p = ParticipantFactory(artist=ArtistFactory(), country=country_rus, contest=contest)

    resp = client.post('/api/v0/votes/',
                       {
                           "from_voter": voter_rus.id,
                           "to_participant": p.id,
                           "point": 12
                       },
                       HTTP_TOKEN=f'{voter_rus.vote_key}')

    status_code = 400
    data = ["You are not allowed to vote for your own country."]

    content = json.loads(resp.content)

    assert resp.status_code == status_code
    assert content == data


@pytest.mark.django_db
def test_vote_with_used_point_and_vote_for_participant_with_point(client, participant_bel, voter_rus):
    VoteFactory(from_voter=voter_rus, to_participant=participant_bel, point=12)

    resp = client.post('/api/v0/votes/',
                       {
                           "from_voter": voter_rus.id,
                           "to_participant": participant_bel.id,
                           "point": 12
                       },
                       HTTP_TOKEN=f'{voter_rus.vote_key}')

    status_code = 400
    data = ["12 point is already given.",
            "You've already given a point to these participant."]

    content = json.loads(resp.content)

    assert resp.status_code == status_code
    assert content == data


@pytest.mark.django_db
def test_vote_more_than_ten_times(client, contest, participant_bel, voter_rus):
    # Populate the db with test data, it's important to use the same voter.
    for i in range(10):
        p = ParticipantFactory(artist=ArtistFactory(), country=CountryFactory(), contest=contest)
        VoteFactory(from_voter=voter_rus, to_participant=p)

    resp = client.post('/api/v0/votes/',
                       {
                           "from_voter": voter_rus.id,
                           "to_participant": participant_bel.id,
                           "point": 12
                       },
                       HTTP_TOKEN=f'{voter_rus.vote_key}')

    status_code = 400
    data = ["You've voted 10 times."]

    content = json.loads(resp.content)

    assert len(Vote.objects.all()) == 10
    assert resp.status_code == status_code
    assert content == data
