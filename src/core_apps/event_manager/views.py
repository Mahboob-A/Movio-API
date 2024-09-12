import logging
import json 

from django.http import JsonResponse
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError as Django_ValidationError


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError as DRF_ValidationError

from celery import chain 

from core_apps.event_manager.utils import save_video_local_storage
from core_apps.event_manager.models import VideoMetaData
from core_apps.event_manager.serializers import VideoMetaDataSerializer
from core_apps.event_manager.tasks import (
    upload_video_to_s3,
    delete_local_video_file_after_s3_upload,
)
from core_apps.event_manager.utils import validate_video_file 


logger = logging.getLogger(__name__)


class VideoUploadAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        video_file = request.FILES.get("video")
        if not video_file:
            return Response(
                {"status": "error", "message": "No video file provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        is_valid, message = validate_video_file(video_file_size=video_file.size, video_file_format=video_file.content_type)
        if not is_valid:
            return Response(
                {"status": "error", 
                 "message": message
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Locaal save
        result = save_video_local_storage(request)

        if result["status"] is True:
            video_file_extention = result["video_file_extention"]
            video_filename_without_extention = result[
                "video_filename_without_extention"
            ]
            local_video_path_with_extention = result["local_video_path_with_extention"]
            local_video_path_without_extention = result[
                "local_video_path_without_extention"
            ]
            db_data = result["db_data"]
        elif result["status"] is False:
            return Response(
                {
                    "status": "error",
                    "detail": "It's not you, it's us! Something unexpected happeded at our end!'",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        try:
            # /movio-temp-videos/
            video_file_extention_without_dot = video_file_extention.split(".")[1]

            s3_file_path = f"{settings.MOVIO_S3_VIDEO_ROOT}/{video_filename_without_extention}/{video_file_extention_without_dot}"

            serializer = VideoMetaDataSerializer(data=db_data)

            if serializer.is_valid(raise_exception=True):
                video_metadata = serializer.save()

                video_processing_chain = chain(
                    upload_video_to_s3.s(
                        local_video_path_with_extention,
                        s3_file_path,
                        video_metadata.id,
                        video_file.size,
                        video_file.content_type,
                    ), 
                    delete_local_video_file_after_s3_upload.s(
                    ),
                )

                video_processing_chain.apply_async(countdown=1)

                logger.info(
                    f"\n[=> Video Upload API SUCCESS]: Video Offloaed Successfully to Celery Worker."
                )
                return Response({
                            "status": "success",
                            "detail": "upload started", 
                            "video_id": video_metadata.id,
                            # "task_id": task.id, 
                            "video_name_without_extention": video_filename_without_extention,
                            "video_extention": video_file_extention,
                    }, 
                        status=status.HTTP_202_ACCEPTED
                )
        except (Django_ValidationError, DRF_ValidationError) as e:
            error_dict = e.detail 
            logger.error(f"\n[XX Video Upload API ERROR XX]: Something Unexpected Happened.\nException: {str(e)}")
            for key, value in error_dict.items():
                if key == "duration":
                    error_message = value[0]
                    return Response({
                                "status": "error",
                                "message": "Invalid video duration. Please provide a valid duration in format: HH:MM:SS",
                                "error_key": key,
                                "detail": json.dumps(error_message)
                        }, 
                        status=status.HTTP_400_BAD_REQUEST
                )
        # General Error Repsonse
        return Response(
            {
                    "status": "error",
                    "detail": "It's not you, It's Us. Unexpected error occurred.",
            }, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
