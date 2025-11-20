"""Kafka consumer for processing patient vitals."""
from backend.services.streaming_service import StreamingService
from backend.streaming.processor import VitalsProcessor
from backend.core.config import settings
from loguru import logger
from typing import Callable, Optional


class VitalsConsumer:
    """Consumer for patient vitals stream."""

    def __init__(self):
        """Initialize vitals consumer."""
        self.streaming_service = StreamingService()
        self.processor = VitalsProcessor()

    def start_consuming(
        self,
        callback: Optional[Callable] = None,
        max_messages: Optional[int] = None
    ):
        """
        Start consuming vitals from Kafka.

        Args:
            callback: Optional custom callback function
            max_messages: Maximum messages to consume (None = infinite)
        """
        topics = [settings.KAFKA_TOPIC_PATIENT_VITALS]

        def handle_message(message_data: dict):
            """Handle incoming vitals message."""
            try:
                # Process through processor
                asyncio.run(self.processor.process_vitals(message_data))

                # Call custom callback if provided
                if callback:
                    callback(message_data)

            except Exception as e:
                logger.error(f"Error handling message: {e}")

        logger.info(f"Starting vitals consumer for topics: {topics}")
        self.streaming_service.consume_messages(
            topics=topics,
            callback=handle_message,
            max_messages=max_messages
        )


import asyncio  # Import at top level for asyncio.run
