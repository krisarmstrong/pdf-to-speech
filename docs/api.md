# API Documentation

## Main Application

**Script**: `pdf_to_speech.py`

Convert PDF documents to MP3 audio files.

### Usage

```bash
python pdf_to_speech.py <input_file> <output_file> [OPTIONS]
```

**Arguments**:
- `input_file`: Path to input PDF file
- `output_file`: Path to output MP3 file

**Options**:
- `--engine <gtts|pyttsx3>`: TTS engine (default: gtts)
- `-v, --verbose`: Enable verbose logging
- `--logfile <path>`: Log file path (default: pdf_to_speech.log)

**Examples**:
```bash
# Using gTTS (requires internet)
python pdf_to_speech.py document.pdf audio.mp3 --engine gtts

# Using pyttsx3 (offline)
python pdf_to_speech.py document.pdf audio.mp3 --engine pyttsx3 --verbose
```

## TTS Engines

### gTTS (Google Text-to-Speech)

- **Pros**: Natural voice, high quality
- **Cons**: Requires internet connection
- **Languages**: 100+ languages supported
- **Rate limits**: Google API limits apply

### pyttsx3 (Offline)

- **Pros**: No internet needed, fast
- **Cons**: Synthetic voice, platform-dependent
- **Engines**: eSpeak (Linux), SAPI5 (Windows), NSSpeechSynthesizer (Mac)

## Dependencies

- PyPDF2 or pdfplumber: PDF text extraction
- gTTS: Google Text-to-Speech
- pyttsx3: Offline text-to-speech
- ffmpeg: Audio processing (if needed)

## Return Codes

- `0`: Success
- `1`: PDF read error
- `2`: Audio generation error
- `3`: Invalid arguments

---
Author: Kris Armstrong
