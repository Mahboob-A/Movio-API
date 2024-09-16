import logging
import json
from typing import Dict, List, Tuple, Union, Any, Set  # noqa
from uuid import UUID

from django.http import HttpRequest
from django.conf import settings
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
    publish_s3_metadata_to_mq,
)


logger = logging.getLogger(__name__)


class VideoUploadAPIView(APIView):
    permission_classes = [
        AllowAny
    ]  #  Authentitication is enforced in middleware level. See Middlewares for more details.

    def process_video_for_local_storage(self, request: HttpRequest) -> Dict[str, str]:
        """Process and save video file to local storage

        Returns:
            - result (dict): result of the video file save operation
        """

        # Locaal save
        result = save_video_local_storage(request)

        if result["status"] is False:
            return Response(
                {
                    "status": "error",
                    "detail": "It's not you, it's us! Something unexpected happeded at our end!'",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return result

    def create_video_event_and_response(
        self,
        request: HttpRequest,
        result: Dict[str, str],
        video_file_size: int,
        video_file_content_type: str,
    ) -> Response:
        """Create video event and response
        Create db entry, and MQ event to be processed by Movio-Worker-Service
        """

        video_file_extention = result["video_file_extention"]
        video_filename_without_extention = result["video_filename_without_extention"]
        video_filename_with_extention = result["video_filename_with_extention"]
        local_video_path_with_extention = result["local_video_path_with_extention"]
        local_video_path_without_extention = result[
            "local_video_path_without_extention"
        ]
        db_data = result["db_data"]

        try:
            # /movio-temp-videos/
            video_file_extention_without_dot = video_file_extention.split(".")[1]

            s3_file_key = f"{settings.MOVIO_S3_VIDEO_ROOT}/{video_filename_without_extention}/{video_file_extention_without_dot}/{video_filename_with_extention}"

            serializer = VideoMetaDataSerializer(data=db_data)

            if serializer.is_valid(raise_exception=True):
                video_metadata = serializer.save()

                # Celery Pipeline: Video Upload to S3 -> Delete Local Video File -> Publish MQ Event
                mq_data = {
                    "user_id": request.payload.get("user_id"),
                    "email": request.payload.get("user_data").get("email"),
                }
                video_processing_chain_events = chain(
                    upload_video_to_s3.s(
                        local_video_path_with_extention,
                        s3_file_key,
                        video_metadata.id,
                        video_file_content_type,
                        video_filename_with_extention,
                    ),
                    delete_local_video_file_after_s3_upload.s(),
                    publish_s3_metadata_to_mq.s(mq_data),
                )
                video_processing_chain_events.apply_async(countdown=1)

                logger.info(
                    f"\n[=> Video Upload API SUCCESS]: Video Offloaed Successfully to Celery Worker."
                )
                return Response(
                    {
                        "status": "success",
                        "detail": "upload started",
                        "video_id": video_metadata.id,
                        "video_name_without_extention": video_filename_without_extention,
                        "video_extention": video_file_extention,
                    },
                    status=status.HTTP_202_ACCEPTED,
                )
        except (Django_ValidationError, DRF_ValidationError) as e:
            error_dict = e.detail
            logger.error(
                f"\n[XX Video Upload API ERROR XX]: Data Validation Error.\nException: {str(e)}"
            )
            for key, value in error_dict.items():
                if key == "duration":
                    error_message = value[0]
                    return Response(
                        {
                            "status": "error",
                            "message": "Invalid video duration. Please provide a valid duration in format: HH:MM:SS",
                            "error_key": key,
                            "detail": json.dumps(error_message),
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

        # General Error Repsonse
        logger.error(
            f"\n[XX Video Upload API ERROR XX]: Something Unexpected Happened.\nException: {str(e)}"
        )
        return Response(
            {
                "status": "error",
                "detail": "It's not you, It's Us. Unexpected error occurred.",
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    def post(self, request: HttpRequest, format=None) -> Response:
        """API to upload video file to Movio-API-Service

        NOTE: Detailed Doc is only intended for code review purpose by external reviewers. It may be removed.

        Authentication:
            - Bearer Token

        Request Body:
            - video_file (file): video file to be uploaded
            - video_name (str): video name
            - video_duration (str): video duration in format: HH:MM:SS
            - video_description (str

        Events:
            - DB Enrty
            - Video S3 Upload
            - MQ Event to be processed by Movio-Worker-Service

        Response:
            - status (str): status of the request
            - detail (str): detail of the request
            - video_id (str): video id
            - video_name_without_extention (str): video name without extention
            - video_extention (str): video extention
        """

        # Authentication and Request Body validations are mapped in two separate middleware. See Middlesares for more details.

        video_file_size = request.video_file_size
        video_file_content_type = request.video_file_content_type

        print("content type: ", video_file_content_type)

        # save video in tmp file for furthur processing
        result = self.process_video_for_local_storage(request=request)

        # final db entry, (activate celery pipeline for s3 upload and mq events), and response
        return self.create_video_event_and_response(
            request=request,
            result=result,
            video_file_size=video_file_size,
            video_file_content_type=video_file_content_type,
        )
