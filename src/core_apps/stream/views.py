from uuid import UUID
from django.http import HttpRequest

from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

from core_apps.event_manager.models import VideoMetaData
from core_apps.stream.renderers import (
    VideoMetaDataJSONRenderer,
    VideosMetadataJSONRenderer,
)
from core_apps.stream.serializers import (
    VideoMetaDataGETSerializer,
    VideoMetaDataListAPIViewSerializer,
)
from core_apps.stream.paginations import VideoMetaDataPageNumberPagination # noqa 


class GetVideoMetadataAPIView(APIView):
    """API View to retrieeve video metadata along with subtitles"""

    permission_classes = [AllowAny]
    renderer_classes = [VideoMetaDataJSONRenderer]

    def get(self, request: HttpRequest, video_id: UUID, format=None) -> Response:
        try:
            video_meatadata = VideoMetaData.objects.get(id=video_id)
        except VideoMetaData.DoesNotExist:
            return Response(
                {"status": "error", "detail": "Video not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = VideoMetaDataGETSerializer(video_meatadata)
        return Response(
            {"status": "success", "detail": serializer.data}, status=status.HTTP_200_OK
        )


class AllVideosListView(ListAPIView):
    """API View to retrieeve all videos metadata"""

    permission_classes = [AllowAny]
    renderer_classes = [VideosMetadataJSONRenderer]
    pagination_class = VideoMetaDataPageNumberPagination

    queryset = VideoMetaData.objects.all()
    serializer_class = VideoMetaDataListAPIViewSerializer
