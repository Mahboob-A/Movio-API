import logging
import os 

from functools import lru_cache


from celery_progress.backend import ProgressRecorder
from botocore.exceptions import ClientError
from botocore import config
import boto3

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1) # more or less works in singleton fashipn
def get_s3_client():
    try:
        return boto3.client("s3", config=config.Config(max_pool_connections=20))
    except ClientError as e:
        logger.error(f"Failed to create S3 client: {str(e)}")
        raise

class S3UploadProgressRecorder:
    """A helper class to record the upload progress of a file to S3."""

    def __init__(self, filepath, task):
        self._filepath = filepath
        self._filesize = float(os.path.getsize(filepath))
        self._current_bytes_upload = 0
        self.progress_recorder = ProgressRecorder(task=task)

    def __call__(self, bytes_transfarrad):
        self._current_bytes_upload += bytes_transfarrad
        uploaded_bytes = (self._current_bytes_upload / self._filesize) * 100
        self.progress_recorder.set_progress(
            uploaded_bytes,
            self._filesize,
            description=f"Uploading {self._filepath} to S3",
        )
