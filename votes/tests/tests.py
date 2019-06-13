# -*-  -*-
# Automated test of the api
import pytest
from .factories import CountryFactory

import json
from .factories import ContestFactory


# 1
# test countries response get's a 200 code:
@pytest.mark.django_db  # -- This is a helper and it is necessary to mark a that this test function is requiring the database.
def test_countries_endpoint(client):
    new_country = CountryFactory()
    response = client.get(f'/api/v0/countries/{new_country.id}', follow=True)
    assert response.status_code == 200


# 2
# test contests response get's a 200 code, and the host_coountry and the year api returned is the we actually want:
@pytest.mark.django_db
def test_contests_endpoint(client):
    new_contest = ContestFactory()
    response = client.get(f'/api/v0/contests/{new_contest.id}', follow=True)
    content = json.loads(response.content)
    assert response.status_code == 200
    assert content['host_country'] == new_contest.host_country.id
    assert content['year'] == new_contest.year
