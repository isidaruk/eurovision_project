from rest_framework.routers import DefaultRouter

from voters.api.views import VoterViewSet


router = DefaultRouter()
router.register('', VoterViewSet)  # , base_name='voters')
urlpatterns = router.urls
