
from django.urls import path 

from core_apps.es_search.views import (
    VideoMetaDataESSearchView,
    SubtitleESSearchView
)

urlpatterns = [
    path("video-metadata/", VideoMetaDataESSearchView.as_view({"get": "list"}, name="video_metadata_es_view")),
    path("subtitle/", SubtitleESSearchView.as_view({"get": "list"}, name="subtitle_es_view")),
          
]
