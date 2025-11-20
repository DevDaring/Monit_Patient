"""Task: Compare with external research papers."""
from typing import Dict, Any
from backend.core.database import db
from loguru import logger


async def compare_external_research(query: str, context: Dict[str, Any], model: str) -> Dict[str, Any]:
    """
    Compare patient case with external medical research.

    Uses:
    - Google Gemini with grounding search for recent research
    - CSV database of research paper summaries
    """
    try:
        from backend.services.gemini_service import GeminiService
        gemini_service = GeminiService()

        # Load external research from CSV
        research_data = db.read_csv("research/external_papers/sepsis_studies.csv")
        cardiac_research = db.read_csv("research/external_papers/cardiac_studies.csv")
        respiratory_research = db.read_csv("research/external_papers/respiratory_studies.csv")

        # Prepare research context
        research_context = {
            "sepsis_studies": research_data.to_dict('records') if not research_data.empty else [],
            "cardiac_studies": cardiac_research.to_dict('records') if not cardiac_research.empty else [],
            "respiratory_studies": respiratory_research.to_dict('records') if not respiratory_research.empty else []
        }

        # Create prompt for Gemini with grounding
        prompt = f"""
You are analyzing a patient case and comparing it with external medical research.

Query: {query}

Patient Context: {context}

Available Research Database:
{research_context}

Task:
1. Use Google grounding search to find recent relevant medical research
2. Compare with the research database provided
3. Identify similar cases or patterns
4. Extract evidence-based insights

Provide:
- Relevant studies (with citations if available)
- Key findings applicable to this case
- Statistical evidence
- Confidence level

Focus on peer-reviewed, high-quality sources from the last 5 years.
"""

        # Use Gemini with grounding search enabled
        response = await gemini_service.generate_response(
            prompt=prompt,
            model=model,
            context=context,
            use_grounding=True  # Enable Google Search grounding
        )

        return {
            "task": "compare_external_research",
            "findings": response,
            "sources_consulted": {
                "sepsis_studies": len(research_context["sepsis_studies"]),
                "cardiac_studies": len(research_context["cardiac_studies"]),
                "respiratory_studies": len(research_context["respiratory_studies"])
            },
            "grounding_used": True
        }

    except Exception as e:
        logger.error(f"Error in compare_external_research: {e}")
        return {
            "task": "compare_external_research",
            "error": str(e)
        }
