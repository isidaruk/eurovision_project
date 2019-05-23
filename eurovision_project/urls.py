"""eurovision_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path


api_version = 'v0/'
api_url = 'api/' + api_version

api_urlpatterns = [
    path('artists/', include('artists.api.urls')),
    path('participants/', include('participants.api.urls')),
    path('votes/', include('votes.api.urls')),
    path('contests/', include('contests.api.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path(api_url, include(api_urlpatterns)),
]
