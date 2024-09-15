from django.conf import settings

from django.http import JsonResponse
from rest_framework import status

from django.utils.deprecation import MiddlewareMixin

from core_apps.common.jwt_decoder import jwt_decoder


class AuthJWTMiddleware:
    """Middleware to authenticate user using JWT token"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        print("\n\nEntering AuthJWTMiddleware: ", str(request))

        payload, detail, message = jwt_decoder.decode_jwt(request=request)

        if payload is None:
            return JsonResponse(
                {"status": "error", "detail": detail, "message": message},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        request.payload = payload

        response = self.get_response(request)

        return response


class VideoUploadMiddleware:
    """Middleware to validate video file size and content type"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if (
            request.method == "POST" and request.path == settings.VIDEO_UPLOAD_API
        ):  # /api/v1/app/events/video-upload/

            video_file = request.FILES.get("video")

            if video_file is None:
                return JsonResponse(
                    {"status": "error", "detail": "No video file provided"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if video_file.size > settings.MAX_VIDEO_FILE_SIZE:  # 100 MB 
                return JsonResponse(
                    {
                        "status": "error",
                        "detail": f"Video file size exceeds the maximum allowed size of {settings.MAX_VIDEO_FILE_SIZE / (1024 * 1024)} MB",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if video_file.content_type not in settings.ALLOWED_VIDEO_FILE_FORMATS:  # MP4/MOV
                return JsonResponse(
                    {
                        "status": "error",
                        "detail": f"Invalid video file format. Only {', '.join(settings.ALLOWED_VIDEO_FILE_FORMATS)} are allowed.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            request.video_file_size = video_file.size
            request.video_file_content_type = video_file.content_type

        response = self.get_response(request)

        return response
