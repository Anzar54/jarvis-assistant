#!/usr/bin/env python3
"""Main entry point for Jarvis voice assistant."""

import click
from loguru import logger
from src.jarvis import Jarvis


@click.group()
def cli():
    """Jarvis - Windows Voice Assistant."""
    logger.add("logs/jarvis.log", rotation="500 MB")


@cli.command()
@click.option('--duration', default=10, help='Listening duration in seconds')
def listen(duration):
    """Start Jarvis and listen for voice commands."""
    jarvis = Jarvis()
    logger.info(f"🎤 Listening mode - {duration} seconds")
    jarvis.listen_and_respond(duration=duration)


@cli.command()
def interactive():
    """Run Jarvis in interactive mode (text + voice)."""
    jarvis = Jarvis()
    jarvis.interactive_mode()


@cli.command()
def test():
    """Test Jarvis components."""
    logger.info("🧪 Testing Jarvis components...")
    jarvis = Jarvis()
    
    logger.info("Testing audio engine...")
    jarvis.audio.list_devices()
    
    logger.info("Testing TTS...")
    jarvis.tts.speak("Hello! Jarvis is ready.")
    
    logger.info("Testing LLM connection...")
    if jarvis.llm.is_available():
        logger.info("✅ Ollama is running.")
    else:
        logger.warning("⚠️  Ollama is not running. Start it with: ollama serve")
    
    logger.info("✅ All tests passed!")


if __name__ == "__main__":
    cli()
