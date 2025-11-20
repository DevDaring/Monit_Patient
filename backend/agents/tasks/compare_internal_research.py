"""Task: Compare with internal hospital research."""
from typing import Dict, Any
from backend.core.database import db
from loguru import logger


async def compare_internal_research(query: str, context: Dict[str, Any], model: str) -> Dict[str, Any]:
    """
    Compare patient case with internal hospital research and case studies.
    """
    try:
        from backend.services.gemini_service import GeminiService
        gemini_service = GeminiService()

        # Load internal research from CSV
        case_studies = db.read_csv("research/internal_research/case_studies.csv")
        treatment_outcomes = db.read_csv("research/internal_research/treatment_outcomes.csv")

        # Prepare internal research context
        internal_context = {
            "case_studies": case_studies.to_dict('records') if not case_studies.empty else [],
            "treatment_outcomes": treatment_outcomes.to_dict('records') if not treatment_outcomes.empty else []
        }

        prompt = f"""
You are analyzing a patient case using internal hospital research data.

Query: {query}

Patient Context: {context}

Internal Research Database:
{internal_context}

Task:
1. Find similar cases in the hospital's database
2. Compare patient demographics, symptoms, and vitals
3. Review treatment approaches used in similar cases
4. Analyze outcomes achieved

Provide:
- Number of similar cases found
- Key similarities and differences
- Treatment patterns that worked
- Success rates observed
- Hospital-specific insights

This is privileged internal data - focus on patterns within our institution.
"""

        response = await gemini_service.generate_response(
            prompt=prompt,
            model=model,
            context=context
        )

        return {
            "task": "compare_internal_research",
            "findings": response,
            "cases_analyzed": len(internal_context["case_studies"]),
            "treatments_reviewed": len(internal_context["treatment_outcomes"])
        }

    except Exception as e:
        logger.error(f"Error in compare_internal_research: {e}")
        return {
            "task": "compare_internal_research",
            "error": str(e)
        }
