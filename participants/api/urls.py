# from participants.api.views import ParticipantViewSet
# from rest_framework.routers import DefaultRouter


# router = DefaultRouter()
# router.register('', ParticipantViewSet)#, base_name='participants')
# urlpatterns = router.urls


from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from participants.api.views import ParticipantList, ParticipantDetail

urlpatterns = [
    path('', ParticipantList.as_view()),
    path('<int:pk>/', ParticipantDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
