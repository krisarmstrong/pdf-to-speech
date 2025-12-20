# Contributing to PdfToSpeech

## Welcome

Thank you for your interest in contributing to PdfToSpeech!

## Getting Started

### Prerequisites

- Python 3.6 or higher
- pip package manager
- Git

### Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Development Workflow

### Making Changes

1. Create a new branch for your feature or fix
2. Make your changes in the `src/` directory
3. Add or update tests in `tests/`
4. Test with various PDF files
5. Update documentation as needed
6. Commit with clear, descriptive messages

### Code Standards

- Follow PEP 8 style guidelines
- Use type hints where applicable
- Write docstrings for functions
- Handle edge cases (empty PDFs, special characters)
- Optimize for large documents

### Testing

Run tests:
```bash
python -m pytest tests/
```

Test with sample PDFs:
```bash
python src/pdf_to_speech.py tests/sample.pdf output.mp3 --verbose
```

## Pull Request Process

1. Ensure all tests pass
2. Update documentation
3. Test both TTS engines
4. Update CHANGELOG
5. Submit PR with clear description

## Questions?

Feel free to open an issue for questions or discussions.

---
Author: Kris Armstrong
