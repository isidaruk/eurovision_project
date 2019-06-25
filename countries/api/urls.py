from rest_framework.routers import DefaultRouter

from countries.api.views import CountryViewSet

router = DefaultRouter()
router.register('', CountryViewSet)

urlpatterns = router.urls
