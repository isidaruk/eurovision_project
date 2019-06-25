from rest_framework.routers import DefaultRouter

from artists.api.views import ArtistViewSet

router = DefaultRouter()
router.register('', ArtistViewSet)

urlpatterns = router.urls
