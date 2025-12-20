#!/usr/bin/env python3
"""
Tests for PdfToSpeech.
"""
from pathlib import Path

import pytest
from PyPDF2 import PdfWriter

from pdf_to_speech import __version__, extract_pdf_text


@pytest.fixture
def pdf_file(tmp_path):
    """Create a temporary PDF file."""
    pdf_path = tmp_path / "test.pdf"
    output_path = tmp_path / "test.mp3"
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    with open(pdf_path, "wb") as f:
        writer.write(f)
    return pdf_path, output_path


def test_version() -> None:
    """Test version format."""
    try:
        import tomllib  # Python 3.11+
    except ModuleNotFoundError:
        try:
            import tomli as tomllib
        except ModuleNotFoundError:
            expected = "0.0.0"
        else:
            pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
            expected = tomllib.loads(pyproject.read_text())["project"]["version"]
    else:
        pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
        expected = tomllib.loads(pyproject.read_text())["project"]["version"]
    assert __version__ == expected


def test_extract_pdf_text(pdf_file) -> None:
    """Test extracting text from a PDF."""
    pdf_path, _ = pdf_file
    text = extract_pdf_text(str(pdf_path))
    assert text == ""


def test_extract_pdf_text_invalid_file() -> None:
    """Test extracting text from an invalid PDF."""
    with pytest.raises(FileNotFoundError):
        extract_pdf_text("nonexistent.pdf")
