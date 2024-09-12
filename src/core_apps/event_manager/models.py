from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import JSONField

from autoslug import AutoSlugField

from core_apps.common.models import IDTimeStampModel


class VideoMetaData(IDTimeStampModel):
    """Video Metadata class for Videos."""

    custom_video_title = models.CharField(
        verbose_name=_("Custom Video Metadata Title (UUID__title)"), max_length=220
    )
    title = models.CharField(verbose_name=_("Video Title"), max_length=220)
    slug = AutoSlugField(populate_from="title", always_update=True, unique=True)

    description = models.TextField(
        verbose_name=_("Video Description"), blank=True, null=True
    )
    duration = models.DurationField(null=True, blank=True)

    is_processing = models.BooleanField(
        verbose_name=_("Is Processing"), default=True
    )

    is_processing_completed = models.BooleanField(
        verbose_name=_("Is Processing Completed"), default=False
    )

    is_processing_failed = models.BooleanField(
        verbose_name=_("Is Processing Failed"), default=False
    )

    # EX: f"https://{s3_bucket_name}.s3.amazonaws.com/movio-video-segments/{video_name}/extention/manifest.mpd"
    mp4_s3_mpd_url = models.URLField(
        verbose_name=_("S3 URL for mp4 MPD file."),
        max_length=255,
        null=True,
        blank=True,
    )

    mov_s3_mpd_url = models.URLField(
        verbose_name=_("S3 URL for mov MPD file."),
        max_length=255,
        null=True,
        blank=True,
    )

    mp4_gcore_cdn_mpd_url = models.URLField(
        verbose_name=_("MP4: Gcore CDN URL file."),
        max_length=255,
        null=True,
        blank=True,
    )

    mov_gcore_cdn_mpd_url = models.URLField(
        verbose_name=_("MOV: Gcore CDN URL MPD file."),
        max_length=255,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Video Meta Data")
        verbose_name_plural = _("Videos Meta Data")
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["title"])]

    @property
    def video_title(self):
        return self.title

    def __str__(self) -> str:
        return self.title


class Subtitle(models.Model):
    video = models.ForeignKey(
        VideoMetaData, on_delete=models.CASCADE, related_name="subtitles"
    )
    language = models.CharField(max_length=6)
    content = JSONField()  

    def __str__(self):
        return f"{self.video.title} - {self.language}"
