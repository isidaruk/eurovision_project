from voters.models import Voter
from participants.models import Participant


import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db


class TestVote:
    def test_model(self):
        country_obj1 = mixer.blend('countries.Country', name='Israel Test Data')
        country_obj2 = mixer.blend('countries.Country', name='Russia Test Data')
        country_obj3 = mixer.blend('countries.Country', name='Belarus Test Data')

        contest_obj = mixer.blend('contests.Contest', host_country=country_obj1)

        voter_obj = mixer.blend('voters.Voter', country=country_obj2, contest=contest_obj)
        to_participant_obj = mixer.blend('participants.Participant', country=country_obj3, contest=contest_obj)

        vote_obj = mixer.blend('votes.Vote', from_voter=voter_obj, to_participant=to_participant_obj)
        assert vote_obj.pk == 1, 'Should create a Vote instance'

    # def test_init(self):
    #     obj = mixer.blend('votes.Vote')
    #     assert obj.pk == 1, 'Should save an instance'
