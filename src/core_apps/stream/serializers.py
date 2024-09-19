from rest_framework import serializers

from core_apps.event_manager.models import VideoMetaData, Subtitle


class SubtitleSerializer(serializers.ModelSerializer):
    """Serializer for the Subtitle model"""

    class Meta:
        model = Subtitle
        fields = ["language", "content"]


class VideoMetaDataGETSerializer(serializers.ModelSerializer):
    """Serializer for the VideoMetaData model to Get Video Information"""

    subtitles = SubtitleSerializer(many=True, read_only=True)

    class Meta:
        model = VideoMetaData
        fields = [
            "custom_video_title",
            "title",
            "description",
            "duration",
            "mp4_s3_mpd_url",
            "mp4_gcore_cdn_mpd_url",
            "subtitles",
        ]
