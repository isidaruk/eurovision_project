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
from django.urls import include, path, re_path

from rest_framework import permissions
from rest_framework.documentation import include_docs_urls
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .api import router

from django.conf import settings


schema_view = get_schema_view(
    openapi.Info(
        title="Eurovision API",
        default_version='v0',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

api_version = 'v0/'
api_url = 'api/' + api_version

api_urlpatterns = [
    path('', include(router.urls)),
    path('docs/', include_docs_urls(title='Eurovision API')),
    path('artists/', include('artists.api.urls')),
    path('participants/', include('participants.api.urls')),
    path('votes/', include('votes.api.urls')),
    path('contests/', include('contests.api.urls')),
    path('countries/', include('countries.api.urls')),
    re_path('swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('voters/', include('voters.api.urls')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path(api_url, include(api_urlpatterns)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),


    ] + urlpatterns
