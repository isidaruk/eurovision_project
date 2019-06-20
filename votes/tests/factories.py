import factory

from artists.models import Artist
from contests.models import Contest
from countries.models import Country

from participants.models import Participant
from voters.models import Voter
from votes.models import Vote


class ArtistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Artist

    name = factory.Sequence(lambda n: 'Artist {}'.format(n))


class CountryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Country

    name = factory.Sequence(lambda n: 'Country {}'.format(n))


class ContestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contest

    year = factory.Sequence(lambda n: 1956 + n)
    host_country = factory.SubFactory(CountryFactory)


class ParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Participant

    artist = factory.SubFactory(ArtistFactory)
    country = factory.SubFactory(CountryFactory)

    song = factory.Faker('word')

    contest = factory.SubFactory(ContestFactory)


class VoterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Voter

    country = factory.SubFactory(CountryFactory)
    contest = factory.SubFactory(ContestFactory)
    vote_key = factory.Faker('uuid4')


class VoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vote

    from_voter = factory.SubFactory(VoterFactory)
    to_participant = factory.SubFactory(ParticipantFactory)

    point = factory.Iterator([1, 2, 3, 4, 5, 6, 7, 8, 10, 12])
