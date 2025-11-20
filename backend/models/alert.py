"""Alert data model."""
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class Alert(BaseModel):
    """Alert data model."""
    alert_id: str
    patient_id: str
    alert_type: str  # vitals, deterioration, medication, etc.
    severity: str  # low, medium, high, critical
    message: str
    details: Optional[Dict[str, Any]] = None
    status: str = "active"  # active, acknowledged, resolved
    created_by: str = "system"  # system or user_id
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    acknowledged_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "alert_id": "A001",
                "patient_id": "P001",
                "alert_type": "vitals",
                "severity": "high",
                "message": "Elevated heart rate detected (125 bpm)",
                "status": "active",
                "timestamp": "2025-01-15T14:35:00"
            }
        }
