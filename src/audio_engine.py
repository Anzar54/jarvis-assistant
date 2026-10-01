"""Audio capture and playback engine for Jarvis."""

import pyaudio
import numpy as np
from typing import Optional, Callable
from loguru import logger
import threading


class AudioEngine:
    """Handles microphone input and speaker output."""

    def __init__(self, sample_rate: int = 16000, chunk_size: int = 1024):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.is_listening = False
        self.audio_data = []
        self.p = pyaudio.PyAudio()

    def list_devices(self) -> None:
        """Print available audio devices."""
        info = self.p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')
        logger.info(f"Available audio devices:")
        for i in range(0, numdevices):
            device_info = self.p.get_device_info_by_host_api_device_index(0, i)
            logger.info(f"  {i}: {device_info.get('name')} - Channels: {device_info.get('maxInputChannels')}")

    def start_listening(self, on_audio: Optional[Callable] = None, duration: int = 10) -> np.ndarray:
        """Capture audio from microphone."""
        logger.info(f"🎤 Listening for {duration} seconds...")
        self.audio_data = []
        self.is_listening = True

        stream = self.p.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
        )

        frames_to_record = int(self.sample_rate / self.chunk_size * duration)

        try:
            for _ in range(frames_to_record):
                if not self.is_listening:
                    break
                data = stream.read(self.chunk_size, exception_on_overflow=False)
                audio_chunk = np.frombuffer(data, dtype=np.float32)
                self.audio_data.append(audio_chunk)

                if on_audio:
                    on_audio(audio_chunk)
        finally:
            stream.stop_stream()
            stream.close()
            self.is_listening = False

        if self.audio_data:
            return np.concatenate(self.audio_data)
        return np.array([])

    def stop_listening(self) -> None:
        """Stop the audio capture."""
        self.is_listening = False
        logger.info("⏹️  Stopped listening.")

    def play_audio(self, audio_data: np.ndarray) -> None:
        """Play audio through speaker."""
        stream = self.p.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.sample_rate,
            output=True,
        )
        stream.write(audio_data.astype(np.float32).tobytes())
        stream.stop_stream()
        stream.close()

    def cleanup(self) -> None:
        """Cleanup audio resources."""
        self.p.terminate()
        logger.info("🎧 Audio engine cleaned up.")
