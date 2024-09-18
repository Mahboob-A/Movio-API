import logging
from typing import Callable

import pika

from django.conf import settings

logger = logging.getLogger(__name__)


class CloudAMQPHandler:
    """CloudAMQP Handler Class to Handle RabbitMQ Connections"""

    def __init__(self) -> None:
        self.broker_url = settings.CLOUD_AMQP_URL
        self.params = pika.URLParameters(self.broker_url)

    def connect(self):
        self.__connection = pika.BlockingConnection(parameters=self.params)
        self.channel = self.__connection.channel()

    def prepare_exchange_and_queue(self) -> None:
        self.channel.exchange_declare(
            exchange=settings.MOVIO_PROCESSED_VIDEO_RESULT_SUBMISSION_EXCHANGE_NAME,
            exchange_type=settings.MOVIO_PROCESSED_VIDEO_RESULT_EXCHANGE_TYPE,
        )

        self.channel.queue_declare(
            queue=settings.MOVIO_PROCESSED_VIDEO_RESULT_QUEUE_NAME
        )

        self.channel.queue_bind(
            settings.MOVIO_PROCESSED_VIDEO_RESULT_QUEUE_NAME,
            settings.MOVIO_PROCESSED_VIDEO_RESULT_SUBMISSION_EXCHANGE_NAME,
            settings.MOVIO_PROCESSED_VIDEO_RESULT_BINDING_KEY,
        )


class VideoProcessResultConsumerMQ(CloudAMQPHandler):
    """Interface calss to Consume messages from
    Movio Worker Service [Video Processed Result: manifest.mpd S3 URL and EN Subtitle VTT]
    """

    def consume_messages(self, callback: Callable) -> None:
        try:
            self.connect()
            self.prepare_exchange_and_queue()

            self.channel.basic_consume(
                settings.MOVIO_PROCESSED_VIDEO_RESULT_QUEUE_NAME,
                callback,
                auto_ack=True,
            )

            logger.info(
                f"\n\n[=> MQ Video Processed Result Consumer LISTEN]: Message Consumption from Movio Worker Service [Video Processed Result: manifest.mpd S3 URL and EN Subtitle VTT] - Started.\n"
            )
            self.channel.start_consuming()

        except Exception as e:
            logger.exception(
                f"\n\n[XX MQ Video Processed Result Consumer EXCEPTION]: Exception Occurred During Cnsuming Messages  Movio Worker Service [Video Processed Result: manifest.mpd S3 URL and EN Subtitle VTT]\n[EXCEPTION]: {str(e)}\n"
            )


video_process_result_consumer_mq = VideoProcessResultConsumerMQ()
