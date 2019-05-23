from django.urls import path

from artists.api.views import ArtistList, ArtistDetail


urlpatterns = [
    path('', ArtistList.as_view()),
    path('<int:pk>/', ArtistDetail.as_view()),
]
