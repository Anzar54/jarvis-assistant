# Detailed Setup Guide for Windows

## Step 1: Install Python

1. Download Python 3.10+ from [python.org](https://www.python.org)
2. During installation, **check "Add Python to PATH"**
3. Verify installation:
   ```bash
   python --version
   ```

## Step 2: Install Visual C++ Build Tools

Some packages require compilation. Install:
- [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/downloads/)

Or use Windows 10/11's built-in developer tools:
```bash
pip install pipwin
```

## Step 3: Install Ollama

1. Download from [ollama.ai](https://ollama.ai)
2. Run the installer
3. Verify installation:
   ```bash
   ollama --version
   ```

## Step 4: Start Ollama Service

```bash
ollama serve
```

In another terminal, pull a model:
```bash
ollama pull mistral
```

## Step 5: Set up Jarvis

```bash
# Clone repo
git clone https://github.com/Anzar54/jarvis-assistant.git
cd jarvis-assistant

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pipwin install pyaudio  # On Windows

# Test
python main.py test
```

## Step 6: Run Jarvis

```bash
python main.py interactive
```

## Troubleshooting

### "pyaudio module not found"
```bash
pip install pipwin
pipwin install pyaudio
```

### "Ollama not available"
Make sure `ollama serve` is running in another terminal.

### No microphone input
Edit `config.yaml` and change `device_index` to match your microphone (check with `python main.py test`).

### Slow performance
Use a smaller Whisper model:
```yaml
STT:
  model_size: "tiny"  # Instead of "base"
```
