from rest_framework.routers import DefaultRouter

from contests.api.views import ContestViewSet


router = DefaultRouter()
router.register('', ContestViewSet)#, base_name='contests')
urlpatterns = router.urls
