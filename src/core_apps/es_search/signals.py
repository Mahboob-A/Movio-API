
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_elasticsearch_dsl.registries import registry

from core_apps.event_manager.models import VideoMetaData, Subtitle



@receiver(post_save, sender=VideoMetaData)
def update_videometadata_es_index(sender, instance=None, created=False, **kwargs):
    registry.update(instance)


@receiver(post_delete, sender=VideoMetaData)
def delete_videometadata_es_index(sender, instance=None, **kwargs):
    registry.delete(instance)


@receiver(post_save, sender=Subtitle)
def update_subtitle_es_index(sender, instance=None, created=False, **kwargs):
    registry.update(instance)


@receiver(post_delete, sender=Subtitle)
def delete_subtitle_es_index(sender, instance=None, **kwargs):
    registry.delete(instance)