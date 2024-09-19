from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from core_apps.es_search.documents import VideoMetaDataDocument, SubtitleDocument


class VideoMetaDataDocumentSerializer(DocumentSerializer):
    """Serializer for VideoMetaDataDocument"""

    class Meta:
        document = VideoMetaDataDocument
        fields = (
            "id", 
            "title",
            "description",
            "created_at",
            "updated_at",
        )


class SubtitleDocumentSerializer(DocumentSerializer):
    """Serializer for SubtitleDocument"""

    class Meta:
        document = SubtitleDocument
        fields = (
            "id", 
            "language",
            "content",
            "created_at",
            "updated_at",
        )
