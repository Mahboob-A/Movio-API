from django.urls import path

from core_apps.stream.views import GetVideoMetadataAPIView

urlpatterns = [
        path("video/<uuid:video_id>/", GetVideoMetadataAPIView.as_view(), name="get_video_metadata"),
]
