from django.urls import path

from rest_framework.urlpatterns import (
    format_suffix_patterns,
)

from participants.api.views import (
    ParticipantDetail,
    ParticipantList,
)

urlpatterns = [
    path('', ParticipantList.as_view()),
    path('<int:pk>/', ParticipantDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
