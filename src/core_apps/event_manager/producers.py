# python
import json
import logging
import os

# pika
import pika

# django
from django.conf import settings

logger = logging.getLogger(__name__)


class CloudAMQPHandler:
    """CloudAMQP Helper Class to Declare Exchange and Queue
    for S3 Video Upload Events
    """

    def __init__(self) -> None:
        self.broker_url = settings.CLOUD_AMQP_URL
        self.params = pika.URLParameters(self.broker_url)

    def connect(self):
        self.__connection = pika.BlockingConnection(parameters=self.params)
        self.channel = self.__connection.channel()

    def prepare_exchange_and_queue(self) -> None:

        self.channel.exchange_declare(
            exchange=settings.MOVIO_RAW_VIDEO_SUBMISSION_EXCHANGE_NAME,
            exchange_type=settings.MOVIO_RAW_VIDEO_SUBMISSION_EXCHANGE_TYPE,
        )
        self.channel.queue_declare(
            queue=settings.MOVIO_RAW_VIDEO_SUBMISSION_QUEUE_NAME
        )

        self.channel.queue_bind(
            settings.MOVIO_RAW_VIDEO_SUBMISSION_QUEUE_NAME,
            settings.MOVIO_RAW_VIDEO_SUBMISSION_EXCHANGE_NAME,
            settings.MOVIO_RAW_VIDEO_SUBMISSION_BINDING_KEY,
        )


class S3MetaDataUploadPublisherMQ(CloudAMQPHandler):
    """Interface Class to Publish Message to Publish Code Submission Queue"""

    def publish_data(self, s3_data: json) -> None:

        try:
            self.connect()
            self.prepare_exchange_and_queue()

            self.channel.basic_publish(
                exchange=settings.MOVIO_RAW_VIDEO_SUBMISSION_EXCHANGE_NAME,
                routing_key=settings.MOVIO_RAW_VIDEO_SUBMISSION_ROUTING_KEY,
                body=s3_data,
            )
            logger.info(
                f"\n\n[=> MQ S3 Metadata Publish SUCCESS]: S3 Data MQ Publish Success.\n\n"
            )
            message = "s3-metadata-mq-publish-success."
            return True, message
        except Exception as e:
            logger.exception(
                f"\n[XX MQ S3 Metadata Publish ERROR XX]: S3 Data MQ Publish Unsuccessful.\n[MQ EXCEPTION]: {str(e)}\n\n"
            )
            message = "s3-metadata-mq-publish-error"
            return False, message


s3_metadata_publisher_mq = S3MetaDataUploadPublisherMQ()
