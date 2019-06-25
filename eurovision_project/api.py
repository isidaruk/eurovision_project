from rest_framework import routers

from artists.api.views import ArtistViewSet
from contests.api.views import ContestViewSet
from countries.api.views import CountryViewSet
from voters.api.views import VoterViewSet

router = routers.DefaultRouter()

router.register('artists', ArtistViewSet)
router.register('contests', ContestViewSet)
router.register('countries', CountryViewSet)
router.register('voters', VoterViewSet)
