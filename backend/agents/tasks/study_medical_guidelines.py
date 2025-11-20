"""Task: Study and apply medical guidelines."""
from typing import Dict, Any
from backend.core.database import db
from loguru import logger


async def study_medical_guidelines(query: str, context: Dict[str, Any], model: str) -> Dict[str, Any]:
    """
    Reference clinical guidelines and protocols.
    """
    try:
        from backend.services.gemini_service import GeminiService
        gemini_service = GeminiService()

        # Load medical guidelines from CSV
        guidelines = db.read_csv("guidelines/medical_guidelines.csv")
        protocols = db.read_csv("guidelines/emergency_protocols.csv")
        drug_interactions = db.read_csv("guidelines/drug_interactions.csv")

        guidelines_context = {
            "clinical_guidelines": guidelines.to_dict('records') if not guidelines.empty else [],
            "emergency_protocols": protocols.to_dict('records') if not protocols.empty else [],
            "drug_interactions": drug_interactions.to_dict('records') if not drug_interactions.empty else []
        }

        prompt = f"""
You are a medical guidelines specialist reviewing a patient case.

Query: {query}

Patient Context: {context}

Available Guidelines and Protocols:
{guidelines_context}

Task:
1. Identify applicable clinical practice guidelines
2. Check relevant emergency protocols
3. Verify treatment standards
4. Review drug interactions (if medications mentioned)
5. Assess compliance with best practices

Provide:
- Relevant guidelines that apply
- Protocol recommendations
- Best practice alignment
- Any contraindications or warnings
- Quality of care indicators

Focus on evidence-based, standard-of-care recommendations.
"""

        response = await gemini_service.generate_response(
            prompt=prompt,
            model=model,
            context=context
        )

        return {
            "task": "study_medical_guidelines",
            "findings": response,
            "guidelines_consulted": len(guidelines_context["clinical_guidelines"]),
            "protocols_reviewed": len(guidelines_context["emergency_protocols"]),
            "drug_interactions_checked": len(guidelines_context["drug_interactions"])
        }

    except Exception as e:
        logger.error(f"Error in study_medical_guidelines: {e}")
        return {
            "task": "study_medical_guidelines",
            "error": str(e)
        }
