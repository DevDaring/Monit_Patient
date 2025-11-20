"""Vital signs data model."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class VitalSigns(BaseModel):
    """Vital signs data model."""
    vital_id: Optional[str] = None
    patient_id: str
    heart_rate: float  # bpm
    bp_systolic: float  # mmHg
    bp_diastolic: float  # mmHg
    o2_saturation: float  # percentage
    temperature: float  # Celsius
    respiratory_rate: Optional[float] = None  # breaths per minute
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "patient_id": "P001",
                "heart_rate": 82,
                "bp_systolic": 120,
                "bp_diastolic": 80,
                "o2_saturation": 98.5,
                "temperature": 37.2,
                "respiratory_rate": 16,
                "timestamp": "2025-01-15T14:30:00"
            }
        }
