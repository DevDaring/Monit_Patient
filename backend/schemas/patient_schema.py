"""Patient schemas for API."""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class PatientCreate(BaseModel):
    """Schema for creating a patient."""
    patient_id: str
    name: str
    age: int
    gender: str
    blood_type: Optional[str] = None
    diagnosis: Optional[str] = None
    assigned_doctor: Optional[str] = None


class PatientResponse(BaseModel):
    """Schema for patient response."""
    patient_id: str
    name: str
    age: int
    gender: str
    blood_type: Optional[str] = None
    diagnosis: Optional[str] = None
    assigned_doctor: Optional[str] = None
    status: str
    room_number: Optional[str] = None


class VitalsCreate(BaseModel):
    """Schema for creating vital signs."""
    patient_id: str
    heart_rate: float
    bp_systolic: float
    bp_diastolic: float
    o2_saturation: float
    temperature: float
    respiratory_rate: Optional[float] = None


class VitalsResponse(BaseModel):
    """Schema for vitals response."""
    patient_id: str
    heart_rate: float
    bp_systolic: float
    bp_diastolic: float
    o2_saturation: float
    temperature: float
    respiratory_rate: Optional[float] = None
    timestamp: datetime


class RiskScoreResponse(BaseModel):
    """Schema for risk score response."""
    patient_id: str
    risk_score: int
    risk_level: str
    concerns: List[str]
    latest_vitals: Optional[dict] = None
