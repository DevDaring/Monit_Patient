"""Kafka topic management."""
from backend.core.config import settings
from loguru import logger


class TopicManager:
    """Manage Kafka topics."""

    TOPICS = {
        'vitals': settings.KAFKA_TOPIC_PATIENT_VITALS,
        'alerts': settings.KAFKA_TOPIC_ALERTS,
        'agent_logs': settings.KAFKA_TOPIC_AGENT_LOGS
    }

    @classmethod
    def get_topic(cls, topic_name: str) -> str:
        """Get topic name by key."""
        return cls.TOPICS.get(topic_name, '')

    @classmethod
    def list_topics(cls) -> dict:
        """List all configured topics."""
        return cls.TOPICS

    @classmethod
    def validate_topics(cls) -> bool:
        """Validate that all topics are configured."""
        for name, topic in cls.TOPICS.items():
            if not topic or topic.startswith('your-'):
                logger.warning(f"Topic '{name}' not properly configured: {topic}")
                return False
        return True
