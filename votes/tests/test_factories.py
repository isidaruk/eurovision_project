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
    name = fake.word()


class CountryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Country

    # fields
    name = fake.word()


class ContestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contest

    # fields
    # year =
    host_country = factory.SubFactory(CountryFactory)


class ParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Voter

    # fields
    artist = factory.SubFactory(ArtistFactory)
    country = factory.SubFactory(CountryFactory)

    song = factory.word()
    contest = factory.SubFactory(ContestFactory)


class VoterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Voter

    # fields
    country = factory.SubFactory(CountryFactory)
    contest = factory.SubFactory(ContestFactory)
    # vote_key =


class VoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vote

    # fields
    from_voter = factory.SubFactory(VoterFactory)
    to_participant = factory.SubFactory(ParticipantFactory)
    # point =
