from django.urls import path 

from core_apps.event_manager.views import VideoUploadAPIView

urlpatterns = [
    path("video/upload/", VideoUploadAPIView.as_view(), name="upload_video"),
]
