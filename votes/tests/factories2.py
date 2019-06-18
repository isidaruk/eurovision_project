import factory

from pytest_factoryboy import register

from artists.models import Artist
from contests.models import Contest
from countries.models import Country
from participants.models import Participant
from votes.models import Vote
from voters.models import Voter


class ArtistFactory(factory.DjangoModelFactory):
    class Meta:
        model = Artist


class ContestFactory(factory.DjangoModelFactory):
    class Meta:
        model = Contest


class CountryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Country


class ParticipantFactory(factory.DjangoModelFactory):
    class Meta:
        model = Participant


class VoteFactory(factory.DjangoModelFactory):
    class Meta:
        model = Vote


class VoterFactory(factory.DjangoModelFactory):
    class Meta:
        model = Voter


register(ArtistFactory)
register(ContestFactory)
register(CountryFactory)
register(ParticipantFactory)
register(VoteFactory)
register(VoterFactory)
