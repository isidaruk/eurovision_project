# from rest_framework.routers import DefaultRouter

# from votes.api.views import VoteViewSet


# router = DefaultRouter()
# router.register('', VoteViewSet)#, base_name='votes')
# urlpatterns = router.urls


from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from votes.api.views import VoteList, VoteDetail

urlpatterns = [
    path('', VoteList.as_view()),
    path('<int:pk>/', VoteDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
