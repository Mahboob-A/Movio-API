from rest_framework import serializers

from core_apps.event_manager.models import VideoMetaData


class VideoMetaDataSerializer(serializers.ModelSerializer):
    """Serializer for the VideoMetaData model."""
    
    class Meta:
        model = VideoMetaData
        fields = [
            "custom_video_title",
            "title",
            "description",
            "duration",
        ]
