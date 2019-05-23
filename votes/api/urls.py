from rest_framework.routers import DefaultRouter

from votes.api.views import VoteViewSet


router = DefaultRouter()
router.register('', VoteViewSet)#, base_name='votes')
urlpatterns = router.urls
