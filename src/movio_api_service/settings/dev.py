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


########################################################

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
