"""Patient data model."""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Patient(BaseModel):
    """Patient data model."""
    patient_id: str
    name: str
    age: int
    gender: str
    blood_type: Optional[str] = None
    admission_date: datetime
    assigned_doctor: Optional[str] = None
    room_number: Optional[str] = None
    diagnosis: Optional[str] = None
    medical_history: Optional[str] = None
    allergies: Optional[str] = None
    medications: Optional[str] = None
    emergency_contact: Optional[str] = None
    status: str = "active"  # active, discharged, critical
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "patient_id": "P001",
                "name": "John Doe",
                "age": 65,
                "gender": "male",
                "blood_type": "A+",
                "admission_date": "2025-01-15T10:30:00",
                "assigned_doctor": "Dr. Smith",
                "room_number": "ICU-201",
                "diagnosis": "Pneumonia",
                "status": "active"
            }
        }
