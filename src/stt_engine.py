"""Speech-to-Text engine for Jarvis."""

import numpy as np
from faster_whisper import WhisperModel
from loguru import logger
from typing import Optional


class STTEngine:
    """Converts audio to text using Whisper."""

    def __init__(self, model_size: str = "base", language: str = "en"):
        self.model_size = model_size
        self.language = language
        logger.info(f"Loading Whisper model: {model_size}...")
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")
        logger.info("✅ Whisper model loaded.")

    def transcribe(self, audio_data: np.ndarray, sample_rate: int = 16000) -> Optional[str]:
        """Convert audio numpy array to text."""
        if len(audio_data) == 0:
            logger.warning("No audio data to transcribe.")
            return None

        try:
            logger.info("🔄 Transcribing audio...")
            segments, info = self.model.transcribe(
                audio_data,
                language=self.language,
                beam_size=5,
            )
            text = "".join([segment.text for segment in segments]).strip()
            logger.info(f"📝 Transcribed: {text}")
            return text
        except Exception as e:
            logger.error(f"❌ Transcription failed: {e}")
            return None
