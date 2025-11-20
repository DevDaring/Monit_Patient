"""Kafka producer for streaming patient vitals."""
from backend.services.streaming_service import StreamingService
from backend.core.config import settings
from loguru import logger
import asyncio


class VitalsProducer:
    """Producer for patient vitals stream."""

    def __init__(self):
        """Initialize vitals producer."""
        self.streaming_service = StreamingService()

    async def send_vitals(self, patient_id: str, vitals_data: dict):
        """Send vital signs to Kafka topic."""
        try:
            await self.streaming_service.produce_vitals(
                patient_id=patient_id,
                vitals_data=vitals_data
            )
            logger.debug(f"Sent vitals for patient {patient_id}")
        except Exception as e:
            logger.error(f"Error sending vitals: {e}")

    async def send_batch_vitals(self, vitals_list: list):
        """Send batch of vital signs."""
        for vitals in vitals_list:
            patient_id = vitals.get('patient_id')
            if patient_id:
                await self.send_vitals(patient_id, vitals)
                # Small delay to avoid overwhelming the system
                await asyncio.sleep(0.1)
