"""Chat message data model."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ChatMessage(BaseModel):
    """Chat message data model."""
    message_id: str
    patient_id: Optional[str] = None
    user_id: str
    role: str  # user, agent, system
    content: str
    audio_url: Optional[str] = None
    language: str = "en"
    metadata: Optional[dict] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "message_id": "M001",
                "patient_id": "P001",
                "user_id": "U001",
                "role": "user",
                "content": "What is the patient's current status?",
                "language": "en",
                "timestamp": "2025-01-15T14:40:00"
            }
        }
