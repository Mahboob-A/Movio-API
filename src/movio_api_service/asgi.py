"""
ASGI config for movio_api_service project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# TODO: Change settings to .production in prod environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "movio_api_service.settings.dev")

application = get_asgi_application()
