"""
URL configuration for movio_api_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path(f"{settings.ADMIN_URL}", admin.site.urls),
    
    # API for Common app - Healthcheck 
    path("api/v1/common/", include("core_apps.common.urls")),
    
    # API of Upload Video Events 
    path("api/v1/app/events/", include("core_apps.event_manager.urls")), 
    
    # API of Stream Video
    path("api/v1/app/stream/", include("core_apps.stream.urls")), 

    # ES Search APIs 
    path("api/v1/app/search/", include("core_apps.es_search.urls")),
    
]
