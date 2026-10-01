"""Text-to-Speech engine for Jarvis."""

import pyttsx3
from loguru import logger
from typing import Optional


class TTSEngine:
    """Converts text to speech using pyttsx3."""

    def __init__(self, rate: int = 150, volume: float = 1.0):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)
        logger.info("✅ TTS engine initialized.")

    def speak(self, text: str) -> None:
        """Convert text to speech and play it."""
        if not text:
            logger.warning("No text to speak.")
            return

        try:
            logger.info(f"🔊 Speaking: {text}")
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"❌ TTS failed: {e}")

    def set_voice(self, voice_index: int = 0) -> None:
        """Set the voice to use (0=male, 1=female typically)."""
        voices = self.engine.getProperty('voices')
        if voice_index < len(voices):
            self.engine.setProperty('voice', voices[voice_index].id)
            logger.info(f"Voice set to: {voices[voice_index].name}")
        else:
            logger.warning(f"Voice index {voice_index} not available.")
