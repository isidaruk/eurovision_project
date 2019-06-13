import factory
from faker import Factory

from artists.models import Artist
from contests.models import Contest
from countries.models import Country

from participants.models import Participant
from voters.models import Voter
from votes.models import Vote


fake = Factory.create()


class ArtistFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Artist

    # fields
    # name = fake.word()
    name = factory.Sequence(lambda n: 'Artist {}'.format(n))


class CountryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Country

    # fields
    # name = fake.word()
    name = factory.Sequence(lambda n: 'Country {}'.format(n))


class ContestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contest

    # fields
    year = factory.Sequence(lambda n: 1956 + n)
    host_country = factory.SubFactory(CountryFactory)


class ParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Participant

    # fields
    artist = factory.SubFactory(ArtistFactory)
    country = factory.SubFactory(CountryFactory)

    song = fake.word()
    # song = factory.Sequence(lambda n: 'Song {}'.format(n))
    contest = factory.SubFactory(ContestFactory)


class VoterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Voter

    # fields
    country = factory.SubFactory(CountryFactory)
    contest = factory.SubFactory(ContestFactory)
    vote_key = factory.Sequence(lambda n: n)


class VoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vote

    # fields
    from_voter = factory.SubFactory(VoterFactory)
    to_participant = factory.SubFactory(ParticipantFactory)
    # point = 1
    point = factory.Iterator([1, 2, 3, 4, 5, 6, 7, 8, 10, 12])
