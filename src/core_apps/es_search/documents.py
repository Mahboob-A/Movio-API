from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from core_apps.event_manager.models import VideoMetaData, Subtitle


@registry.register_document
class VideoMetaDataDocument(Document):
    """Elasicsearch Document for VideoMetaData Model"""
    
    id = fields.TextField(attr="id")
    title = fields.TextField(attr="title")
    description = fields.TextField(attr="description")
    
    class Index:
        name = "videosmetadata"
        settings = {
                "number_of_shards": 1,
                "number_of_replicas": 0,
        }
        
    class Django:
        model = VideoMetaData
        fields  = ["created_at", "updated_at"]


@registry.register_document
class SubtitleDocument(Document):
    """Elactisearch Document for Subtitle Model"""

    id = fields.TextField(attr="id")
    language = fields.TextField(attr="language")
    content = fields.TextField(attr="content")

    class Index:
        name = "subtitles"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }
    class Django:
        model = Subtitle
        fields = ["created_at", "updated_at"]
