from rest_framework import routers

from artists.api.views import ArtistViewSet
from contests.api.views import ContestViewSet
from countries.api.views import CountryViewSet
from participants.api.views import ParticipantViewSet
from votes.api.views import VoteViewSet


router = routers.DefaultRouter()
router.register('artists', ArtistViewSet)
router.register('contests', ContestViewSet)
router.register('countries', CountryViewSet)
router.register('participants', ParticipantViewSet)
router.register('votes', VoteViewSet)
