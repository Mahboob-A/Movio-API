from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _ 

class EventManagerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core_apps.event_manager"
    verbose_name = _("Event Manager")

    def ready(self) -> None:
        import core_apps.es_search.signals 