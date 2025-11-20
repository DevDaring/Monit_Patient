"""Gemini API service with Google grounding search."""
import google.generativeai as genai
from typing import Dict, Any, Optional
from backend.core.config import settings
from loguru import logger


class GeminiService:
    """Service for interacting with Google Gemini API."""

    def __init__(self):
        """Initialize Gemini service."""
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.default_model = settings.GEMINI_MODEL_NAME

    async def generate_response(
        self,
        prompt: str,
        model: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        use_grounding: bool = False,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate response from Gemini.

        Args:
            prompt: The prompt to send to Gemini
            model: Model name (defaults to config)
            context: Additional context dictionary
            use_grounding: Enable Google Search grounding
            temperature: Temperature for generation
            max_tokens: Max tokens to generate

        Returns:
            Generated text response
        """
        try:
            model_name = model or self.default_model
            temp = temperature if temperature is not None else settings.GEMINI_TEMPERATURE
            max_tok = max_tokens or settings.GEMINI_MAX_TOKENS

            # Initialize model
            model_instance = genai.GenerativeModel(model_name)

            # Build generation config
            generation_config = {
                "temperature": temp,
                "max_output_tokens": max_tok,
            }

            # Add grounding if requested
            tools = None
            if use_grounding:
                # Enable Google Search grounding
                tools = [{"google_search": {}}]

            # Add context to prompt if provided
            full_prompt = prompt
            if context:
                context_str = f"\n\nAdditional Context:\n{context}\n\n"
                full_prompt = context_str + prompt

            # Generate response
            if tools:
                response = model_instance.generate_content(
                    full_prompt,
                    generation_config=generation_config,
                    tools=tools
                )
            else:
                response = model_instance.generate_content(
                    full_prompt,
                    generation_config=generation_config
                )

            # Extract text from response
            if response.candidates:
                return response.text
            else:
                logger.warning("No candidates in Gemini response")
                return "No response generated"

        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return f"Error generating response: {str(e)}"

    async def chat_session(
        self,
        messages: list,
        model: Optional[str] = None
    ) -> str:
        """
        Multi-turn chat session.

        Args:
            messages: List of message dicts with 'role' and 'content'
            model: Model name

        Returns:
            Generated response
        """
        try:
            model_name = model or self.default_model
            model_instance = genai.GenerativeModel(model_name)

            # Start chat
            chat = model_instance.start_chat(history=[])

            # Send messages
            response = None
            for message in messages:
                if message['role'] == 'user':
                    response = chat.send_message(message['content'])

            return response.text if response else "No response"

        except Exception as e:
            logger.error(f"Chat session error: {e}")
            return f"Error in chat: {str(e)}"

    async def analyze_with_grounding(
        self,
        query: str,
        patient_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze patient case with external research grounding.

        Args:
            query: Medical query
            patient_data: Patient context

        Returns:
            Analysis with grounded research
        """
        prompt = f"""
Analyze this medical case using current research and evidence-based medicine.

Patient Data:
{patient_data}

Query: {query}

Use Google Search to find recent, relevant medical research and guidelines.
Provide evidence-based analysis with citations where applicable.
"""

        response = await self.generate_response(
            prompt=prompt,
            use_grounding=True
        )

        return {
            "query": query,
            "analysis": response,
            "grounding_used": True
        }
