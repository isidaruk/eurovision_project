from participants.api.views import ParticipantViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('', ParticipantViewSet)#, base_name='participants')
urlpatterns = router.urls
