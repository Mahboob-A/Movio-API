import logging
import json
import traceback

from django.conf import settings


# from celery import chain, group, chord  # noqa

from core_apps.event_manager.consumers import (
    video_process_result_consumer_mq,
)


logger = logging.getLogger(__name__)


def callback(channel, method, properties, body):
    """Callback to consume messages from Movio API Service"""

    try:
        # body in bytes, decode to str then dict
        mq_consumed_data = json.loads(body.decode("utf-8"))

        logger.info(f"\n\n[=> MQ Consume Started]: MQ Message Consume Started.\n")

        print(f"\n\nConsumer MQ Data: {mq_consumed_data}\n")

        logger.info(f"\n\n[=> MQ Consume Started]: MQ Message Consume Success.\n")

    except Exception as e:
        logger.error(
            f"\n\n[XX MQ Consume Failed XX]: MQ Message Consume Failed.\n"
            f"Error: {str(e)}\n"
            f"Traceback: {traceback.format_exc()}\n"
        )


def main():
    # consuming the messaages from the queue where the Movio Worker Service publishes processed video file result i.e. manifest s3 url, and en subtitle vtt

    video_process_result_consumer_mq.consume_messages(callback=callback)
