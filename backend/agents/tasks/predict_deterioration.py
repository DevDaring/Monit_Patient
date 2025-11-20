"""Task: Predict patient deterioration using ML and pattern recognition."""
from typing import Dict, Any
from backend.core.database import db
from loguru import logger
import pandas as pd


async def predict_deterioration(query: str, context: Dict[str, Any], model: str) -> Dict[str, Any]:
    """
    Predict patient deterioration risk using vital signs patterns.
    """
    try:
        from backend.services.gemini_service import GeminiService
        gemini_service = GeminiService()

        # Extract patient_id from context
        patient_id = context.get('patient_id')

        # Load vitals data
        vitals = db.read_csv("vitals/vitals_history.csv")

        if not vitals.empty and patient_id and 'patient_id' in vitals.columns:
            # Filter for specific patient
            patient_vitals = vitals[vitals['patient_id'] == patient_id]

            # Sort by timestamp to get trajectory
            if 'timestamp' in patient_vitals.columns:
                patient_vitals = patient_vitals.sort_values('timestamp')

            # Calculate trends
            trends = {}
            if not patient_vitals.empty:
                for col in ['heart_rate', 'bp_systolic', 'bp_diastolic', 'o2_saturation', 'temperature']:
                    if col in patient_vitals.columns:
                        values = patient_vitals[col].dropna()
                        if len(values) >= 2:
                            trends[col] = {
                                "current": values.iloc[-1],
                                "previous": values.iloc[-2] if len(values) > 1 else values.iloc[-1],
                                "trend": "increasing" if values.iloc[-1] > values.iloc[0] else "decreasing",
                                "rate_of_change": (values.iloc[-1] - values.iloc[0]) / len(values) if len(values) > 0 else 0
                            }
        else:
            patient_vitals = pd.DataFrame()
            trends = {}

        prompt = f"""
You are a predictive analytics specialist for patient deterioration.

Query: {query}

Patient Context: {context}

Recent Vital Signs (time-ordered):
{patient_vitals.tail(20).to_dict('records') if not patient_vitals.empty else "No vitals data available"}

Calculated Trends:
{trends}

Task:
1. Analyze vital signs trajectories
2. Identify early warning signs
3. Calculate deterioration risk score (0-100)
4. Predict potential timeline
5. Assess confidence in prediction

Provide:
- Risk Score (0-100 with 100 being highest risk)
- Early Warning Signs: List any detected
- Predicted Timeline: Hours/days to potential deterioration
- Confidence Level: Low/Medium/High
- Specific Concerns: What vitals are most concerning
- Recommended Interventions: What should be done

Use established early warning scores (NEWS, MEWS) as reference.
"""

        response = await gemini_service.generate_response(
            prompt=prompt,
            model=model,
            context=context
        )

        return {
            "task": "predict_deterioration",
            "patient_id": patient_id,
            "findings": response,
            "trends_analyzed": trends,
            "vitals_data_points": len(patient_vitals) if not patient_vitals.empty else 0
        }

    except Exception as e:
        logger.error(f"Error in predict_deterioration: {e}")
        return {
            "task": "predict_deterioration",
            "error": str(e)
        }
