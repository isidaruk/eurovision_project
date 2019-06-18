import json
import pytest

from .factories2 import artist_factory, contest_factory, country_factory, participant_factory, vote_factory, voter_factory

from votes.models import Vote

from .factories import (
    ArtistFactory,
    CountryFactory,
    ContestFactory,
    ParticipantFactory,
    VoterFactory,
    VoteFactory,
)


@pytest.fixture
def contest(contest_factory, country_factory):
    return contest_factory(year=2019, host_country=country_factory(name='Israel'))


# test_vote_created
@pytest.mark.django_db
def test_vote_created(client, artist_factory, contest, country_factory, participant_factory, voter_factory):
    v = voter_factory(country=country_factory(name='Russia'), contest=contest)
    p = participant_factory(artist=artist_factory(), country=country_factory(name='Belarus'), contest=contest)

    from_voter = v.id
    to_participant = p.id
    point = 12
    token = v.vote_key

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

    # print('Test data 1:', v.country.name, 'to', p.country.name)

    content = json.loads(resp.content)
    # print(content)

    assert resp.status_code == status_code
    assert content == data


# test_vote_with_invalid_token
@pytest.mark.django_db
def test_vote_with_invalid_token(client, artist_factory, contest, country_factory, participant_factory, voter_factory):
    v = voter_factory(
        country=country_factory(name='Russia'), contest=contest, vote_key='00000000-0000-0000-0000-000000000000'
    )
    p = participant_factory(artist=artist_factory(), country=country_factory(name='Belarus'), contest=contest)

    invalid_token = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'

    resp = client.post('/api/v0/votes/',
                       {
                           "from_voter": v.id,
                           "to_participant": p.id,
                           "point": 12
                       },
                       HTTP_TOKEN=f'{invalid_token}')

    status_code = 403
    data = "You do not have permission to perform this action."

    # print('Test data 2:', v.country.name, 'to', p.country.name, 'got token:', invalid_token, 'expected token:', v.vote_key)

    content = json.loads(resp.content)
    # print(content)

    assert resp.status_code == status_code
    assert content['detail'] == data


# test_vote_for_own_country
@pytest.mark.django_db
def test_vote_for_own_country(client, artist_factory, contest, country_factory, participant_factory, voter_factory):
    country = country_factory(name='Russia')

    v = voter_factory(country=country, contest=contest)
    p = participant_factory(artist=artist_factory(), country=country, contest=contest)

    resp = client.post('/api/v0/votes/',
                       {
                           "from_voter": v.id,
                           "to_participant": p.id,
                           "point": 12
                       },
                       HTTP_TOKEN=f'{v.vote_key}')

    status_code = 400
    data = ["You are not allowed to vote for your own country."]

    # print('Test data 3:', v.country.name, 'to', p.country.name)

    content = json.loads(resp.content)
    # print(content)

    assert resp.status_code == status_code
    assert content == data


# test_vote_with_used_point
# test_vote_for_participant_with_point
@pytest.mark.django_db
def test_vote_with_used_point(client, artist_factory, contest, country_factory, participant_factory, voter_factory, vote_factory):
    country = country_factory(name='Russia')

    v = voter_factory(country=country, contest=contest)
    p = participant_factory(artist=artist_factory(), country=country_factory(name='Belarus'), contest=contest)
    vote = vote_factory(from_voter=v, to_participant=p, point=12)

    resp = client.post('/api/v0/votes/',
                       {
                           "from_voter": v.id,
                           "to_participant": p.id,
                           "point": 12
                       },
                       HTTP_TOKEN=f'{v.vote_key}')

    status_code = 400
    data = ["12 point is already given.",
            "You've already given a point to these participant."]

    # print('Test data 4:', v.country.name, 'to', p.country.name)

    content = json.loads(resp.content)
    # print(content)

    assert resp.status_code == status_code
    assert content == data


# test_vote_more_than_ten_times
@pytest.mark.django_db
def test_vote_more_than_ten_times(client, artist_factory, contest, country_factory, participant_factory, voter_factory, vote_factory):
    country = country_factory(name='Russia')

    v = voter_factory(country=country, contest=contest)
    # p = participant_factory(artist=artist_factory(), country=country_factory(), contest=contest)

    # Populate the db with test data, it's important use the same voter.
    for i in range(10):
        p = participant_factory(artist=artist_factory(name=i), country=country_factory(name=i), contest=contest)
        vote_factory(from_voter=v, to_participant=p)

    resp = client.post('/api/v0/votes/',
                       {
                           "from_voter": v.id,
                           "to_participant": p.id,
                           "point": 12
                       },
                       HTTP_TOKEN=f'{v.vote_key}')

    status_code = 400
    data = ["You've voted 10 times."]

    # print('Test data 5:', v.country.name, 'to', p.country.name)

    content = json.loads(resp.content)
    # print(content)

    assert len(Vote.objects.all()) == 10
    assert resp.status_code == status_code
    assert content == data
