import logging

from celery import shared_task
from django.core.files.storage import default_storage
from django.conf import settings


import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def upload_video_to_s3(self, local_video_filepath, s3_file_path):
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    try:
        s3_client.upload_file(
            local_video_filepath, settings.AWS_STORAGE_BUCKET_NAME, s3_file_path
        )

    except FileNotFoundError as e:
        logger.exception(
            f"\n[XX Video Upload S3 ERROR XX]: The Local VIdeo File: {local_video_filepath} was not Found.\nException: {str(e)}"
        )
    except ClientError as e:
        logger.error(
            f"\n[XX Video Upload S3 ERROR XX]: S3 Client Error.\nException: {str(e)}\nRetrying to upload: {local_video_filepath}"
        )
        # Exponential backoff 
        if self.request.retries < self.max_retries:
            retry_in = 2**self.request.retries
            logger.warning(
                f"\n[## SEGMENT S3 UPLOAD WARNING ]: The Local Video {local_video_filepath} Couldn't be Uploaded.\nRetrying in: {retry_in}."
            )
            raise self.retry(exc=e, countdown=retry_in)
    except Exception as e:
        logger.exception(
            f"\n[XX Video Upload S3 ERROR XX]: Unexpected Error Occurred. Local Video couldn't be uploaded to S3.\nException: {str(e)}"
        )
    return True, "video-upload-successful"
