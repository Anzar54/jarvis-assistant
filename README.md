# Jarvis - Windows Voice Assistant

A local, voice-enabled desktop assistant for Windows with wake-word detection, speech-to-text, AI responses, and text-to-speech.

## Features

✨ **Voice Control**: Speak naturally to Jarvis
🎤 **Push-to-Talk**: Press a hotkey to activate listening
🤖 **Local LLM**: Uses Ollama for offline AI responses
🔊 **Text-to-Speech**: Natural voice responses
⚡ **Fast STT**: Whisper-based transcription
🛠️ **Extensible Commands**: Add custom commands easily

## Requirements

- Windows 10/11
- Python 3.10+
- Microphone
- [Ollama](https://ollama.ai/) (for local LLM)

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/Anzar54/jarvis-assistant.git
cd jarvis-assistant
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install PyAudio (Windows)
```bash
pip install pipwin
pipwin install pyaudio
```

### 5. Install Ollama
Download from [ollama.ai](https://ollama.ai)

### 6. Pull a model
```bash
ollama pull mistral
```

## Quick Start

### Run interactive mode
```bash
python main.py interactive
```

### Run voice listening mode
```bash
python main.py listen --duration 10
```

### Test components
```bash
python main.py test
```

## Configuration

Edit `config.yaml` to customize:
- **Wake word**: Change `jarvis` to your preferred word
- **STT Model**: `tiny`, `base`, `small`, `medium`, `large`
- **LLM Model**: Change from `mistral` to `neural-chat`, `orca-mini`, etc.
- **Voice rate**: Adjust TTS speed
- **Listening mode**: `always-on`, `push-to-talk`, or `wake-word`

## Usage Examples

### Built-in Commands
```
"What time is it?"
"What's today's date?"
"Open notepad"
"Search Python tutorials"
```

### Natural Questions
```
"How do I learn Python?"
"What's the capital of France?"
"Write a haiku about coding"
```

## Project Structure

```
jarvis-assistant/
├── src/
│   ├── audio_engine.py      # Microphone & audio handling
│   ├── stt_engine.py        # Speech-to-text (Whisper)
│   ├── tts_engine.py        # Text-to-speech (pyttsx3)
│   ├── llm_engine.py        # Local LLM (Ollama)
│   ├── commands.py          # Command registry
│   └── jarvis.py            # Main assistant logic
├── main.py                  # CLI entry point
├── config.yaml              # Configuration
├── requirements.txt         # Dependencies
└── README.md               # This file
```

## Troubleshooting

### Ollama not running?
```bash
ollama serve
```

### No audio input?
```python
python main.py test
# Check device list
```

### Slow transcription?
Download a smaller Whisper model: `tiny` or `base`

## Roadmap

- [ ] Always-on listening with wake-word detection (Porcupine/pvporcupine)
- [ ] Global hotkey support (push-to-talk)
- [ ] Advanced command scheduling
- [ ] Integration with Windows apps (Spotify, Weather API, etc.)
- [ ] Conversation memory
- [ ] Multi-language support

## License

MIT

## Author

Anzar54
