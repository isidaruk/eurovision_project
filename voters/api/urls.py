from rest_framework.routers import DefaultRouter

from voters.api.views import VoterViewSet

router = DefaultRouter()
router.register('', VoterViewSet)

urlpatterns = router.urls
