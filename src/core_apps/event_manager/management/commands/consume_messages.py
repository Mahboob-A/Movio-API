from django.core.management.base import BaseCommand

from core_apps.event_manager.consumer_callback import main


class Command(BaseCommand):
    """Consumes Messages from Movio Worker Service  [Video Processed Result: manifest.mpd S3 URL and EN Subtitle VTT]"""

    help = "Consumes messages from RabbitMQ - Published by Movio Worker Service [Video Processed Result: manifest.mpd S3 URL and EN Subtitle VTT]"

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(
                "Consuming messages from Movio Worker Service  [Video Processed Result: manifest.mpd S3 URL and EN Subtitle VTT] ..."
            )
        )
        main()
