from .base import *  # noqa
from .base import env  # noqa: E501


# ########################## Security

SECRET_KEY = "django-insecure-#&$)q+-f$bm++2_m^6^pq=)qnl8g3_p)0dv$bi+nmdzcy^86oh"

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1"]


CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8001",  # Django Developement Server
    "http://127.0.0.1:8081",  # Dockerizedd Django App with Nginx
]

CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8001",  # Django Developement Server
    "http://127.0.0.1:8081",  # Dockerizedd Django App with Nginx
]


# ######################### CELERY CONFIG

CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
# CELERY_ACCEPT_CONTECT = ["json"]
# CELERY_TASK_SERIALIZER = "json"
# CELERY_RESULT_SERIALIZER = "json"
CELERY_RESULT_BACKEND_MAX_RETRIES = 15
CELERY_TASK_SEND_SENT_EVENT = True
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE


# ######################### File Storage

# FILE_UPLOAD_STORAGE = env("FILE_UPLOAD_STORAGE", default="LOCAL") # local and S3



AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")

AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME")
AWS_QUERYSTRING_AUTH = False  # False will make data public
AWS_S3_FILE_OVERWRITE = False

AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"

# MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/"

########################################################

# ########################## S3 Bucket Settings

TEMP_LOCAL_VIDEO_DIR_ROOT = str(BASE_DIR / "movio-local-video-files")
TEMP_LOCAL_VIDEO_DIR = f"{TEMP_LOCAL_VIDEO_DIR_ROOT}/tmp-movio-videos"

MOVIO_S3_VIDEO_ROOT = "movio-temp-videos"

# ########################## Logging


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(name)-12s %(asctime)s %(module)s  %(process)d %(thread)d %(message)s "
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
    # uncomment for django database query logs
    # "loggers": {
    #     "django.db": {
    #         "level": "DEBUG",
    #         "handlers": ["console"],
    #     }
    # },
}
