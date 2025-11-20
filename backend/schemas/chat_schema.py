"""Chat schemas for API."""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChatRequest(BaseModel):
    """Schema for chat request."""
    patient_id: Optional[str] = None
    message: str
    language: str = "en"


class VoiceChatRequest(BaseModel):
    """Schema for voice chat request."""
    patient_id: Optional[str] = None
    language: str = "en"
    # Audio will be sent as file upload


class ChatResponse(BaseModel):
    """Schema for chat response."""
    message_id: str
    content: str
    audio_url: Optional[str] = None
    timestamp: datetime


class VoiceResponse(BaseModel):
    """Schema for voice response."""
    text: str
    audio_url: str
    language: str
