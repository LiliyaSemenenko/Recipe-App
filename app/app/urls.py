"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from django.contrib import admin
# include: helper function that allows to include urls from a different app
from django.urls import path, include

from django.conf.urls.static import static  # import static url
from django.conf import settings  # to retrieve settings

from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/health-check/', core_views.health_check, name='health-check'),

    # api/schema/ url generates schema for our API and uses SpectacularAPIView
    # Schema is a yaml file that describes the API
    # SpectacularAPIView: generates the schema file needed for our project
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path(
        # serves Swagger documentation that will use
        # 'api-schema' to generate a GUI for our API documentation.
        'api/docs/',
        # url_name='api-schema' tells that 'api-schema'
        # should be used (defined above)
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api-docs',
    ),
    path('api/user/', include('user.urls')),
    # include all URLs defined inside /recipes/urls.py
    path('api/recipe/', include('recipe.urls')),
]

# mimic behavior expected from Django dev server
# allow it to serve media files from dev server (not happening by default)
if settings.DEBUG:  # if debug mode (dev server o local machine)
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
