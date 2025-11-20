"""Chat and voice interface endpoints."""
from fastapi import APIRouter, HTTPException, UploadFile, File
from backend.schemas.chat_schema import (
    ChatRequest,
    ChatResponse,
    VoiceResponse
)
from backend.services.voice_service import VoiceService
from backend.services.agent_service import AgentService
from loguru import logger
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/chat", tags=["chat"])
voice_service = VoiceService()
agent_service = AgentService()


@router.post("/text", response_model=ChatResponse)
async def chat_text(request: ChatRequest):
    """
    Text-based chat with agent system.

    Processes text queries and returns text responses.
    """
    try:
        # Build context
        context = {}
        if request.patient_id:
            context['patient_id'] = request.patient_id

        # Process through agent system
        result = await agent_service.process_query(
            query=request.message,
            context=context
        )

        # Extract response
        response_text = result.get('final_response', 'No response generated')

        return ChatResponse(
            message_id=str(uuid.uuid4()),
            content=response_text,
            timestamp=datetime.utcnow()
        )

    except Exception as e:
        logger.error(f"Error in text chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/voice", response_model=VoiceResponse)
async def chat_voice(
    audio: UploadFile = File(...),
    patient_id: str = None,
    language: str = "en"
):
    """
    Voice-based chat with agent system.

    Accepts audio input, processes through agents, returns both text and audio response.
    """
    try:
        # Read audio data
        audio_data = await audio.read()

        # Transcribe audio to text (placeholder - integrate STT service)
        # In production, use Google Speech-to-Text or Gemini's audio capabilities
        transcribed_text = "Placeholder transcription - integrate STT service"

        logger.info(f"Received voice input (length: {len(audio_data)} bytes)")

        # Process through agent system
        context = {}
        if patient_id:
            context['patient_id'] = patient_id

        result = await agent_service.process_query(
            query=transcribed_text,
            context=context
        )

        response_text = result.get('final_response', 'No response generated')

        # Convert response to speech
        audio_bytes = await voice_service.text_to_speech(
            text=response_text,
            language=language
        )

        # In production, save audio to file storage and return URL
        # For now, return placeholder
        audio_url = "/audio/placeholder.mp3"

        return VoiceResponse(
            text=response_text,
            audio_url=audio_url,
            language=language
        )

    except Exception as e:
        logger.error(f"Error in voice chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/text-to-speech")
async def convert_text_to_speech(text: str, language: str = "en"):
    """
    Convert text to speech using ElevenLabs.

    Useful for generating voice responses.
    """
    try:
        audio_bytes = await voice_service.text_to_speech(
            text=text,
            language=language
        )

        # Return audio data (in production, save to storage)
        return {
            "status": "success",
            "audio_length": len(audio_bytes),
            "language": language
        }

    except Exception as e:
        logger.error(f"Error in text-to-speech: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/voices")
async def get_available_voices():
    """Get list of available ElevenLabs voices."""
    try:
        voices = voice_service.get_available_voices()
        return {"voices": voices}
    except Exception as e:
        logger.error(f"Error getting voices: {e}")
        raise HTTPException(status_code=500, detail=str(e))
