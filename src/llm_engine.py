"""Local LLM engine for Jarvis (Ollama-based)."""

import requests
from loguru import logger
from typing import Optional
import json


class LLMEngine:
    """Interfaces with local Ollama LLM."""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "mistral"):
        self.base_url = base_url
        self.model = model
        self.endpoint = f"{base_url}/api/generate"
        logger.info(f"LLM Engine configured for {model} at {base_url}")

    def is_available(self) -> bool:
        """Check if Ollama service is running."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Ollama not available: {e}")
            return False

    def generate(self, prompt: str, temperature: float = 0.7, timeout: int = 30) -> Optional[str]:
        """Generate response from the LLM."""
        if not self.is_available():
            logger.error("❌ Ollama service is not running. Start it with: ollama serve")
            return None

        try:
            logger.info(f"🤖 Generating response for: {prompt}")
            payload = {
                "model": self.model,
                "prompt": prompt,
                "temperature": temperature,
                "stream": False,
            }
            response = requests.post(self.endpoint, json=payload, timeout=timeout)
            response.raise_for_status()
            result = response.json()
            text = result.get("response", "").strip()
            logger.info(f"✅ LLM Response: {text}")
            return text
        except Exception as e:
            logger.error(f"❌ LLM generation failed: {e}")
            return None
