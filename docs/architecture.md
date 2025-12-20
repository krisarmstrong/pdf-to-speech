# Architecture

## Overview

PdfToSpeech is a Python-based document-to-audio conversion tool that transforms PDF text content into MP3 audio files using text-to-speech (TTS) engines.

## System Architecture

### Core Components

1. **Main Converter** (`pdf_to_speech.py`)
   - PDF text extraction
   - Text preprocessing
   - TTS engine integration
   - Audio file generation
   - Logging system

### Technical Implementation

#### PDF Text Extraction

Uses PyPDF2 or pdfplumber for:
- Page-by-page text extraction
- Text encoding handling
- Layout preservation
- Metadata access

#### Text-to-Speech Engines

Supports two TTS backends:

1. **gTTS (Google Text-to-Speech)**
   - Cloud-based synthesis
   - Natural voice quality
   - Multiple language support
   - Internet connection required

2. **pyttsx3 (Offline TTS)**
   - Local synthesis
   - No internet required
   - System voice engines
   - Platform-dependent quality

### Data Flow

```
PDF File → Text Extraction → Text Preprocessing → TTS Engine → Audio Generation → MP3 File
                                  ↓
                          Logging & Progress
```

### Audio Processing

MP3 generation:
- Text chunking for large documents
- Audio concatenation
- Quality settings
- Format conversion

## Design Principles

1. **Flexibility**: Multiple TTS engine support
2. **Accessibility**: Convert documents to audio
3. **Quality**: Configurable audio output
4. **Usability**: Simple CLI interface

---
Author: Kris Armstrong
