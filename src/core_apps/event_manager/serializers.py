from rest_framework import serializers

from core_apps.event_manager.models import VideoMetaData, Subtitle


class VideoMetaDataPOSTSerializer(serializers.ModelSerializer):
    """Serializer for the VideoMetaData model to Create an Instance."""

    class Meta:
        model = VideoMetaData
        fields = [
            "custom_video_title",
            "title",
            "description",
            "duration",
            "user_id", 
            "email", 
            "phone_number", 
        ]


