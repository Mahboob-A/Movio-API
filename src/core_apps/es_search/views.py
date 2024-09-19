from django_elasticsearch_dsl_drf.filter_backends import (
    OrderingFilterBackend,
    FilteringFilterBackend,
    IdsFilterBackend,
    DefaultOrderingFilterBackend,
    CompoundSearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from rest_framework.permissions import IsAuthenticated, AllowAny

from core_apps.es_search.documents import VideoMetaDataDocument, SubtitleDocument
from core_apps.es_search.serializers import (
    VideoMetaDataDocumentSerializer,
    SubtitleDocumentSerializer,
)


class VideoMetaDataESSearchView(DocumentViewSet):
    """Viewset for VideoMetaDataDocument"""

    document = VideoMetaDataDocument
    serializer_class = VideoMetaDataDocumentSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"

    filter_backends = [
        CompoundSearchFilterBackend,
        OrderingFilterBackend,
        FilteringFilterBackend,
        IdsFilterBackend,
        DefaultOrderingFilterBackend,
    ]

    search_fields = (
        "title",
        "description",
    )

    filter_fields = {
        "created_at": "created_at", 
    }

    ordering_fields = {
        "created_at": "created_at",
    }

    ordering = (
        "-created_at"
    )


class SubtitleESSearchView(DocumentViewSet):
    """Viewset for VideoMetaDataDocument"""

    document = SubtitleDocument
    serializer_class = SubtitleDocumentSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"

    filter_backends = [
        CompoundSearchFilterBackend,
        OrderingFilterBackend,
        FilteringFilterBackend,
        IdsFilterBackend,
        DefaultOrderingFilterBackend,
    ]

    search_fields = (
        "language",
        "content",
    )

    filter_fields = {
        "created_at": "created_at"
    }

    ordering_fields = {
        "created_at": "created_at",
    }

    ordering = "-created_at"
