from django.urls import path

from core_apps.stream.views import GetVideoMetadataAPIView, AllVideosListView

urlpatterns = [
    path(
        "video-metadata/<uuid:video_id>/",
        GetVideoMetadataAPIView.as_view(),
        name="get_video_metadata",
    ),
    path("videos/all/", AllVideosListView.as_view(), name="all_videos"),
]
