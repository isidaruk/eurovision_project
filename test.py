import factory
import pytest

from pytest_factoryboy import register
from countries.models import Country


class CountryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Country


register(CountryFactory)


@pytest.mark.parametrize('name', ['Russia', 'Belarus'])
@pytest.mark.django_db
def test_factory_fixture(country_factory, name):
    c = country_factory(name=name)
    assert c.name == name
    assert len(Country.objects.all()) == 1
    assert Country.objects.get(name=name).name == name
