import os 
from celery import Celery 

from django.conf import settings

# TODO: Change the settings environment into .production in production environment 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movio_api_service.settings.dev")

app = Celery("movio_api_service")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

