"""Patient management endpoints."""
from fastapi import APIRouter, HTTPException
from typing import List
from backend.schemas.patient_schema import (
    PatientCreate,
    PatientResponse,
    VitalsCreate,
    VitalsResponse,
    RiskScoreResponse
)
from backend.services.patient_service import PatientService
from loguru import logger

router = APIRouter(prefix="/api/patients", tags=["patients"])
patient_service = PatientService()


@router.get("/", response_model=List[PatientResponse])
async def get_all_patients():
    """Get all patients."""
    try:
        patients = patient_service.get_all_patients()
        return patients
    except Exception as e:
        logger.error(f"Error getting patients: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{patient_id}", response_model=PatientResponse)
async def get_patient(patient_id: str):
    """Get patient by ID."""
    try:
        patient = patient_service.get_patient(patient_id)
        if not patient:
            raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")
        return patient
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting patient {patient_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=dict)
async def create_patient(patient: PatientCreate):
    """Create new patient."""
    try:
        success = patient_service.add_patient(patient.model_dump())
        if success:
            return {"status": "success", "patient_id": patient.patient_id}
        else:
            raise HTTPException(status_code=500, detail="Failed to create patient")
    except Exception as e:
        logger.error(f"Error creating patient: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{patient_id}/vitals", response_model=List[VitalsResponse])
async def get_patient_vitals(patient_id: str, limit: int = 100):
    """Get patient vital signs history."""
    try:
        vitals = patient_service.get_patient_vitals(patient_id, limit)
        return vitals
    except Exception as e:
        logger.error(f"Error getting vitals for patient {patient_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/vitals", response_model=dict)
async def add_vital_signs(vitals: VitalsCreate):
    """Add vital signs record."""
    try:
        success = patient_service.add_vital_signs(vitals.model_dump())
        if success:
            return {"status": "success", "patient_id": vitals.patient_id}
        else:
            raise HTTPException(status_code=500, detail="Failed to add vital signs")
    except Exception as e:
        logger.error(f"Error adding vital signs: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{patient_id}/risk-score", response_model=RiskScoreResponse)
async def get_risk_score(patient_id: str):
    """Get patient risk score."""
    try:
        risk_data = patient_service.calculate_risk_score(patient_id)
        return risk_data
    except Exception as e:
        logger.error(f"Error calculating risk score: {e}")
        raise HTTPException(status_code=500, detail=str(e))
