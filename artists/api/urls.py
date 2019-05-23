from django.urls import path

from artists.api.views import ArtistViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('', ArtistViewSet, base_name='artists')
urlpatterns = router.urls
