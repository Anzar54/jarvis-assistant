"""Main Jarvis voice assistant."""

import yaml
from pathlib import Path
from loguru import logger
from typing import Optional
import sys

from src.audio_engine import AudioEngine
from src.stt_engine import STTEngine
from src.tts_engine import TTSEngine
from src.llm_engine import LLMEngine
from src.commands import CommandRegistry


class Jarvis:
    """Main Jarvis voice assistant."""

    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        logger.info("🤖 Initializing Jarvis...")
        
        # Initialize engines
        self.audio = AudioEngine(
            sample_rate=self.config['Audio']['sample_rate'],
            chunk_size=self.config['Audio']['chunk_size'],
        )
        self.stt = STTEngine(
            model_size=self.config['STT']['model_size'],
            language=self.config['STT']['language'],
        )
        self.tts = TTSEngine(
            rate=self.config['TTS']['rate'],
            volume=self.config['TTS']['volume'],
        )
        self.llm = LLMEngine(
            base_url=self.config['LLM']['base_url'],
            model=self.config['LLM']['model'],
        )
        self.commands = CommandRegistry()
        logger.info("✅ Jarvis initialized successfully.")

    @staticmethod
    def _load_config(config_path: str) -> dict:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"✅ Config loaded from {config_path}")
            return config
        except FileNotFoundError:
            logger.error(f"❌ Config file not found: {config_path}")
            sys.exit(1)

    def listen_and_respond(self, duration: int = 10) -> None:
        """Listen for audio and generate a response."""
        # Capture audio
        audio_data = self.audio.start_listening(duration=duration)
        
        if len(audio_data) == 0:
            self.tts.speak("I didn't hear anything. Please try again.")
            return

        # Transcribe audio
        text = self.stt.transcribe(audio_data, self.config['Audio']['sample_rate'])
        if not text:
            self.tts.speak("I couldn't understand that. Please try again.")
            return

        # Check for built-in commands
        cmd_result = self._try_command(text)
        if cmd_result:
            self.tts.speak(cmd_result)
            return

        # Otherwise, use LLM to generate a response
        response = self.llm.generate(text)
        if response:
            self.tts.speak(response)
        else:
            self.tts.speak("I'm having trouble thinking right now. Please try again later.")

    def _try_command(self, text: str) -> Optional[str]:
        """Try to execute a built-in command from the user's text."""
        text_lower = text.lower()
        
        # Simple command matching
        if any(phrase in text_lower for phrase in ["what time", "tell me time", "current time"]):
            return self.commands.execute("time")
        elif any(phrase in text_lower for phrase in ["what date", "tell me date", "today"]):
            return self.commands.execute("date")
        elif text_lower.startswith("open "):
            app = text_lower.replace("open ", "").strip()
            return self.commands.execute("open", app)
        elif text_lower.startswith("search "):
            query = text_lower.replace("search ", "").strip()
            return self.commands.execute("search", query)
        
        return None

    def interactive_mode(self) -> None:
        """Run Jarvis in interactive mode."""
        self.tts.speak("Jarvis is ready. Press Enter to speak, or type 'quit' to exit.")
        
        while True:
            try:
                user_input = input("\n🎤 You: ").strip()
                if user_input.lower() == "quit":
                    self.tts.speak("Goodbye!")
                    break
                elif user_input == "":
                    print("Listening...")
                    self.listen_and_respond(duration=10)
                else:
                    # Process text input directly
                    cmd_result = self._try_command(user_input)
                    if cmd_result:
                        print(f"Jarvis: {cmd_result}")
                        self.tts.speak(cmd_result)
                    else:
                        response = self.llm.generate(user_input)
                        if response:
                            print(f"Jarvis: {response}")
                            self.tts.speak(response)
            except KeyboardInterrupt:
                print("\n\nShutting down...")
                break
        
        self.cleanup()

    def cleanup(self) -> None:
        """Cleanup resources."""
        self.audio.cleanup()
        logger.info("👋 Jarvis shut down.")
