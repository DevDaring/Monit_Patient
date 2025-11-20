"""Patient data service."""
from typing import List, Dict, Any, Optional
from backend.core.database import db
from loguru import logger
import pandas as pd
from datetime import datetime


class PatientService:
    """Service for patient data operations."""

    def __init__(self):
        """Initialize patient service."""
        self.patients_file = "patients/patient_records.csv"
        self.vitals_file = "vitals/vitals_history.csv"

    def get_all_patients(self) -> List[Dict[str, Any]]:
        """Get all patients."""
        try:
            patients_df = db.read_csv(self.patients_file)
            if patients_df.empty:
                return []
            return patients_df.to_dict('records')
        except Exception as e:
            logger.error(f"Error getting patients: {e}")
            return []

    def get_patient(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """Get single patient by ID."""
        try:
            patients_df = db.read_csv(self.patients_file)
            if patients_df.empty or 'patient_id' not in patients_df.columns:
                return None

            patient = patients_df[patients_df['patient_id'] == patient_id]
            if patient.empty:
                return None

            return patient.iloc[0].to_dict()
        except Exception as e:
            logger.error(f"Error getting patient {patient_id}: {e}")
            return None

    def get_patient_vitals(
        self,
        patient_id: str,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get patient vital signs history."""
        try:
            vitals_df = db.read_csv(self.vitals_file)
            if vitals_df.empty or 'patient_id' not in vitals_df.columns:
                return []

            patient_vitals = vitals_df[vitals_df['patient_id'] == patient_id]

            # Sort by timestamp if available
            if 'timestamp' in patient_vitals.columns:
                patient_vitals = patient_vitals.sort_values('timestamp', ascending=False)

            # Limit results
            patient_vitals = patient_vitals.head(limit)

            return patient_vitals.to_dict('records')
        except Exception as e:
            logger.error(f"Error getting vitals for patient {patient_id}: {e}")
            return []

    def add_patient(self, patient_data: Dict[str, Any]) -> bool:
        """Add new patient."""
        try:
            return db.append_row(self.patients_file, patient_data)
        except Exception as e:
            logger.error(f"Error adding patient: {e}")
            return False

    def update_patient(
        self,
        patient_id: str,
        updates: Dict[str, Any]
    ) -> bool:
        """Update patient information."""
        try:
            return db.update_row(
                self.patients_file,
                patient_id,
                'patient_id',
                updates
            )
        except Exception as e:
            logger.error(f"Error updating patient {patient_id}: {e}")
            return False

    def add_vital_signs(self, vitals_data: Dict[str, Any]) -> bool:
        """Add vital signs record."""
        try:
            # Add timestamp if not present
            if 'timestamp' not in vitals_data:
                vitals_data['timestamp'] = datetime.utcnow().isoformat()

            return db.append_row(self.vitals_file, vitals_data)
        except Exception as e:
            logger.error(f"Error adding vital signs: {e}")
            return False

    def calculate_risk_score(self, patient_id: str) -> Dict[str, Any]:
        """
        Calculate patient risk score based on latest vitals.

        Returns risk score 0-100 and risk level.
        """
        try:
            vitals = self.get_patient_vitals(patient_id, limit=1)
            if not vitals:
                return {"risk_score": 0, "risk_level": "unknown", "reason": "No vitals data"}

            latest = vitals[0]
            risk_score = 0
            concerns = []

            # Simple risk scoring (you can make this more sophisticated)
            # Heart rate
            hr = latest.get('heart_rate', 0)
            if hr > 120 or hr < 50:
                risk_score += 30
                concerns.append(f"Abnormal heart rate: {hr}")

            # Blood pressure
            bp_sys = latest.get('bp_systolic', 0)
            if bp_sys > 180 or bp_sys < 90:
                risk_score += 25
                concerns.append(f"Abnormal blood pressure: {bp_sys}")

            # Oxygen saturation
            o2 = latest.get('o2_saturation', 100)
            if o2 < 92:
                risk_score += 35
                concerns.append(f"Low oxygen saturation: {o2}%")

            # Temperature
            temp = latest.get('temperature', 37.0)
            if temp > 38.5 or temp < 36.0:
                risk_score += 10
                concerns.append(f"Abnormal temperature: {temp}°C")

            # Determine risk level
            if risk_score >= 70:
                risk_level = "critical"
            elif risk_score >= 50:
                risk_level = "high"
            elif risk_score >= 30:
                risk_level = "medium"
            else:
                risk_level = "low"

            return {
                "patient_id": patient_id,
                "risk_score": min(risk_score, 100),
                "risk_level": risk_level,
                "concerns": concerns,
                "latest_vitals": latest
            }

        except Exception as e:
            logger.error(f"Error calculating risk score: {e}")
            return {"risk_score": 0, "risk_level": "error", "reason": str(e)}
