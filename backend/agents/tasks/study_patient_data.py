"""Task: Study batch patient data for patterns."""
from typing import Dict, Any
from backend.core.database import db
from loguru import logger
import pandas as pd


async def study_patient_data(query: str, context: Dict[str, Any], model: str) -> Dict[str, Any]:
    """
    Analyze patterns across multiple patients.
    """
    try:
        from backend.services.gemini_service import GeminiService
        gemini_service = GeminiService()

        # Load patient data from CSV
        patients = db.read_csv("patients/patient_records.csv")
        vitals = db.read_csv("vitals/vitals_history.csv")

        # Perform basic statistical analysis
        stats = {}
        if not patients.empty:
            stats["total_patients"] = len(patients)
            if 'age' in patients.columns:
                stats["avg_age"] = patients['age'].mean()
            if 'gender' in patients.columns:
                stats["gender_distribution"] = patients['gender'].value_counts().to_dict()

        if not vitals.empty and 'heart_rate' in vitals.columns:
            stats["avg_heart_rate"] = vitals['heart_rate'].mean()
            stats["avg_bp_systolic"] = vitals.get('bp_systolic', pd.Series([0])).mean()
            stats["avg_o2_sat"] = vitals.get('o2_saturation', pd.Series([0])).mean()

        prompt = f"""
You are analyzing batch patient data to identify patterns and trends.

Query: {query}

Patient Context: {context}

Available Data:
- Total Patients: {stats.get('total_patients', 0)}
- Patient Demographics: {patients.head(10).to_dict('records') if not patients.empty else []}
- Vitals Statistics: {stats}
- Recent Vitals: {vitals.head(20).to_dict('records') if not vitals.empty else []}

Task:
1. Identify patterns across patients
2. Find statistical correlations
3. Compare patient groups
4. Generate insights

Provide:
- Data patterns identified
- Statistical significance
- Risk factors across population
- Comparative insights
- Actionable recommendations
"""

        response = await gemini_service.generate_response(
            prompt=prompt,
            model=model,
            context=context
        )

        return {
            "task": "study_patient_data",
            "findings": response,
            "statistics": stats,
            "patients_analyzed": len(patients) if not patients.empty else 0
        }

    except Exception as e:
        logger.error(f"Error in study_patient_data: {e}")
        return {
            "task": "study_patient_data",
            "error": str(e)
        }
