"""ElevenLabs voice service for text-to-speech and speech-to-text."""
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from typing import Optional
from backend.core.config import settings
from loguru import logger
import io


class VoiceService:
    """Service for ElevenLabs voice interface."""

    def __init__(self):
        """Initialize ElevenLabs client."""
        self.client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)
        self.default_voice_id = settings.ELEVENLABS_VOICE_ID
        self.model = settings.ELEVENLABS_MODEL

    async def text_to_speech(
        self,
        text: str,
        voice_id: Optional[str] = None,
        language: str = "en"
    ) -> bytes:
        """
        Convert text to speech.

        Args:
            text: Text to convert
            voice_id: ElevenLabs voice ID
            language: Language code (en, hi, bn, etc.)

        Returns:
            Audio bytes
        """
        try:
            vid = voice_id or self.default_voice_id

            # Generate speech
            audio = self.client.generate(
                text=text,
                voice=vid,
                model=self.model,
                voice_settings=VoiceSettings(
                    stability=settings.ELEVENLABS_STABILITY,
                    similarity_boost=settings.ELEVENLABS_SIMILARITY_BOOST
                )
            )

            # Convert generator to bytes
            audio_bytes = b"".join(audio)

            logger.info(f"Generated speech for text (length: {len(text)})")
            return audio_bytes

        except Exception as e:
            logger.error(f"Text-to-speech error: {e}")
            raise

    async def speech_to_text(
        self,
        audio_data: bytes
    ) -> str:
        """
        Convert speech to text (transcription).

        Note: ElevenLabs primarily does TTS. For STT, you might want to use
        Google Speech-to-Text or Gemini's audio capabilities.

        For now, this is a placeholder that could integrate with Gemini.
        """
        try:
            # Placeholder: In production, use Google Speech-to-Text or Gemini
            # For demo, return placeholder
            logger.warning("Speech-to-text not fully implemented, using placeholder")

            # In production, you would use:
            # - Google Cloud Speech-to-Text API
            # - Or Gemini's audio processing
            # - Or Whisper API

            return "Transcription placeholder - integrate STT service"

        except Exception as e:
            logger.error(f"Speech-to-text error: {e}")
            raise

    async def generate_multilingual_response(
        self,
        text: str,
        language: str = "en",
        voice_id: Optional[str] = None
    ) -> bytes:
        """
        Generate multilingual voice response.

        Supports: English, Hindi, Bengali, and more.

        Args:
            text: Text to speak
            language: Language code
            voice_id: Voice ID (uses multilingual voices)

        Returns:
            Audio bytes
        """
        # ElevenLabs' multilingual models automatically handle different languages
        return await self.text_to_speech(text, voice_id, language)

    def get_available_voices(self) -> list:
        """Get list of available voices."""
        try:
            voices = self.client.voices.get_all()
            return [
                {
                    "voice_id": voice.voice_id,
                    "name": voice.name,
                    "category": voice.category if hasattr(voice, 'category') else None
                }
                for voice in voices.voices
            ]
        except Exception as e:
            logger.error(f"Error getting voices: {e}")
            return []
