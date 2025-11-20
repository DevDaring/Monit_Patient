"""Task: Deep dive into individual patient data."""
from typing import Dict, Any
from backend.core.database import db
from loguru import logger
import pandas as pd


async def study_individual_data(query: str, context: Dict[str, Any], model: str) -> Dict[str, Any]:
    """
    Comprehensive analysis of a single patient.
    """
    try:
        from backend.services.gemini_service import GeminiService
        gemini_service = GeminiService()

        # Extract patient_id from context
        patient_id = context.get('patient_id')

        if not patient_id:
            return {
                "task": "study_individual_data",
                "error": "No patient_id provided in context"
            }

        # Load patient-specific data
        patients = db.read_csv("patients/patient_records.csv")
        vitals = db.read_csv("vitals/vitals_history.csv")

        # Filter for specific patient
        patient_info = patients[patients['patient_id'] == patient_id] if not patients.empty and 'patient_id' in patients.columns else pd.DataFrame()
        patient_vitals = vitals[vitals['patient_id'] == patient_id] if not vitals.empty and 'patient_id' in vitals.columns else pd.DataFrame()

        # Sort vitals by timestamp if available
        if not patient_vitals.empty and 'timestamp' in patient_vitals.columns:
            patient_vitals = patient_vitals.sort_values('timestamp', ascending=False)

        prompt = f"""
You are performing a comprehensive analysis of a single patient.

Query: {query}

Patient ID: {patient_id}

Patient Information:
{patient_info.to_dict('records') if not patient_info.empty else "No patient data found"}

Vitals History (most recent first):
{patient_vitals.head(50).to_dict('records') if not patient_vitals.empty else "No vitals data found"}

Additional Context: {context}

Task:
1. Review complete medical profile
2. Analyze vital signs trajectory over time
3. Identify personal risk factors
4. Track trends and changes

Provide:
- Patient profile summary
- Key risk factors (personal)
- Vital signs evolution analysis
- Recent concerning changes (if any)
- Personalized care recommendations

Focus on this individual patient's unique circumstances.
"""

        response = await gemini_service.generate_response(
            prompt=prompt,
            model=model,
            context=context
        )

        return {
            "task": "study_individual_data",
            "patient_id": patient_id,
            "findings": response,
            "vitals_records_analyzed": len(patient_vitals) if not patient_vitals.empty else 0,
            "patient_found": not patient_info.empty
        }

    except Exception as e:
        logger.error(f"Error in study_individual_data: {e}")
        return {
            "task": "study_individual_data",
            "error": str(e)
        }
