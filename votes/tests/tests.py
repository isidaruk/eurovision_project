# -*-  -*-
# Automated test of the api
import pytest
from .factories import CountryFactory


# 1
# test countries response get's a 200 code:
@pytest.mark.django_db  # -- This is a helper and it is necessary to mark a that this test function is requiring the database.
def test_countries_endpoint(client):
    new_country = CountryFactory()
    response = client.get(f'/api/v0/countries/{new_country.id}', follow=True)
    assert response.status_code == 200
