"""Confluent Kafka streaming service."""
from confluent_kafka import Producer, Consumer, KafkaError, KafkaException
from typing import Dict, Any, Callable, Optional
from backend.core.config import settings
from loguru import logger
import json


class StreamingService:
    """Service for Confluent Cloud Kafka streaming."""

    def __init__(self):
        """Initialize Kafka producer and consumer configs."""
        self.producer_config = {
            'bootstrap.servers': settings.CONFLUENT_BOOTSTRAP_SERVERS,
            'sasl.mechanisms': 'PLAIN',
            'security.protocol': 'SASL_SSL',
            'sasl.username': settings.CONFLUENT_API_KEY,
            'sasl.password': settings.CONFLUENT_API_SECRET,
        }

        self.consumer_config = {
            **self.producer_config,
            'group.id': settings.KAFKA_CONSUMER_GROUP,
            'auto.offset.reset': 'latest',
            'enable.auto.commit': True
        }

        self.producer = None
        self.consumer = None

    def get_producer(self) -> Producer:
        """Get or create Kafka producer."""
        if not self.producer:
            try:
                self.producer = Producer(self.producer_config)
                logger.info("Kafka producer initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Kafka producer: {e}")
                raise
        return self.producer

    def get_consumer(self, topics: list) -> Consumer:
        """Get or create Kafka consumer."""
        try:
            consumer = Consumer(self.consumer_config)
            consumer.subscribe(topics)
            logger.info(f"Kafka consumer subscribed to topics: {topics}")
            return consumer
        except Exception as e:
            logger.error(f"Failed to initialize Kafka consumer: {e}")
            raise

    def delivery_report(self, err, msg):
        """Kafka delivery callback."""
        if err is not None:
            logger.error(f'Message delivery failed: {err}')
        else:
            logger.debug(f'Message delivered to {msg.topic()} [{msg.partition()}]')

    async def produce_vitals(
        self,
        patient_id: str,
        vitals_data: Dict[str, Any]
    ):
        """Produce patient vitals to Kafka topic."""
        try:
            producer = self.get_producer()

            message = {
                "patient_id": patient_id,
                **vitals_data
            }

            producer.produce(
                topic=settings.KAFKA_TOPIC_PATIENT_VITALS,
                key=patient_id,
                value=json.dumps(message),
                callback=self.delivery_report
            )

            producer.poll(0)  # Trigger delivery callbacks

            logger.info(f"Produced vitals for patient {patient_id}")

        except Exception as e:
            logger.error(f"Error producing vitals: {e}")
            raise

    async def produce_alert(
        self,
        alert_data: Dict[str, Any]
    ):
        """Produce alert to Kafka topic."""
        try:
            producer = self.get_producer()

            producer.produce(
                topic=settings.KAFKA_TOPIC_ALERTS,
                key=alert_data.get('patient_id', 'unknown'),
                value=json.dumps(alert_data),
                callback=self.delivery_report
            )

            producer.poll(0)

            logger.info(f"Produced alert for patient {alert_data.get('patient_id')}")

        except Exception as e:
            logger.error(f"Error producing alert: {e}")
            raise

    async def produce_agent_log(
        self,
        log_data: Dict[str, Any]
    ):
        """Produce agent activity log to Kafka topic."""
        try:
            producer = self.get_producer()

            producer.produce(
                topic=settings.KAFKA_TOPIC_AGENT_LOGS,
                value=json.dumps(log_data),
                callback=self.delivery_report
            )

            producer.poll(0)

        except Exception as e:
            logger.error(f"Error producing agent log: {e}")

    def consume_messages(
        self,
        topics: list,
        callback: Callable[[Dict[str, Any]], None],
        max_messages: Optional[int] = None
    ):
        """
        Consume messages from Kafka topics.

        Args:
            topics: List of topics to consume from
            callback: Function to call with each message
            max_messages: Maximum messages to consume (None = infinite)
        """
        consumer = self.get_consumer(topics)
        count = 0

        try:
            while max_messages is None or count < max_messages:
                msg = consumer.poll(timeout=1.0)

                if msg is None:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        logger.error(f"Consumer error: {msg.error()}")
                        break

                # Parse message
                try:
                    message_data = json.loads(msg.value().decode('utf-8'))
                    callback(message_data)
                    count += 1
                except Exception as e:
                    logger.error(f"Error processing message: {e}")

        except KeyboardInterrupt:
            logger.info("Consumer interrupted")
        finally:
            consumer.close()

    def flush_producer(self):
        """Flush pending producer messages."""
        if self.producer:
            self.producer.flush()
