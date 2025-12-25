#!/usr/bin/env python3
"""
Project Title: PdfToSpeech

Converts PDF documents to MP3 audio files using gTTS or pyttsx3.

Author: Kris Armstrong
"""
import argparse
import logging
import sys
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version
from logging.handlers import RotatingFileHandler
from pathlib import Path

import pyttsx3
from gtts import gTTS
from PyPDF2 import PdfReader


def _find_pyproject(start: Path) -> Path | None:
    for parent in (start, *start.parents):
        candidate = parent / "pyproject.toml"
        if candidate.is_file():
            return candidate
    return None


def _read_pyproject_version() -> str:
    try:
        import tomllib  # Python 3.11+
    except ModuleNotFoundError:
        return "0.0.0"

    pyproject = _find_pyproject(Path(__file__).resolve())
    if not pyproject:
        return "0.0.0"
    try:
        data = tomllib.loads(pyproject.read_text())
    except Exception:
        return "0.0.0"
    return data.get("project", {}).get("version", "0.0.0")


_pyproject_version = _read_pyproject_version()
if _pyproject_version != "0.0.0":
    __version__ = _pyproject_version
else:
    try:
        __version__ = _pkg_version("pdf-to-speech")
    except PackageNotFoundError:
        __version__ = "0.0.0"


class Config:
    """Global constants for PdfToSpeech."""

    LOG_FILE: str = "pdf_to_speech.log"
    ENCODING: str = "utf-8"


def setup_logging(verbose: bool, logfile: str = Config.LOG_FILE) -> None:
    """Configure logging with rotating file handler.

    Args:
        verbose: Enable DEBUG level logging if True.
        logfile: Path to log file.

    Raises:
        PermissionError: If log file cannot be written.
    """
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            RotatingFileHandler(logfile, maxBytes=1048576, backupCount=3),
            logging.StreamHandler(),
        ],
    )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Convert PDF files to MP3 audio using gTTS or pyttsx3.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("input_file", help="Input PDF file")
    parser.add_argument("output_file", help="Output MP3 file")
    parser.add_argument(
        "--engine",
        choices=["gtts", "pyttsx3"],
        default="gtts",
        help="Text-to-speech engine (gtts requires internet)",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--logfile", default=Config.LOG_FILE, help="Log file path")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser.parse_args()


def extract_pdf_text(input_file: str) -> str:
    """Extract text from a PDF file.

    Args:
        input_file: Path to PDF file.

    Returns:
        Extracted text as a string.

    Raises:
        FileNotFoundError: If input file doesn't exist.
        PermissionError: If input file cannot be read.
    """
    logging.info("Reading PDF file: %s", input_file)
    try:
        with open(input_file, "rb") as f:
            pdf_reader = PdfReader(f)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text() or ""
                text += page_text
            clean_text = text.replace("\n", " ").strip()
            logging.debug("Extracted text length: %d characters", len(clean_text))
            return clean_text
    except FileNotFoundError:
        logging.error("Input file not found: %s", input_file)
        raise
    except PermissionError as e:
        logging.error("Cannot read input file %s: %s", input_file, e)
        raise
    except Exception as e:
        logging.error("Error extracting text from PDF: %s", e)
        raise


def google_text_to_speech(text: str, output_file: str) -> None:
    """Convert text to speech using gTTS and save as MP3.

    Args:
        text: Text to convert.
        output_file: Path to output MP3 file.

    Raises:
        PermissionError: If output file cannot be written.
        Exception: If gTTS fails (e.g., network issues).
    """
    logging.info("Converting text to speech with gTTS: %s", output_file)
    try:
        tts = gTTS(text, lang="en")
        tts.save(output_file)
        logging.info("MP3 file written: %s", output_file)
    except PermissionError as e:
        logging.error("Cannot write to output file %s: %s", output_file, e)
        raise
    except Exception as e:
        logging.error("gTTS conversion failed: %s", e)
        raise


def pyttsx3_text_to_speech(text: str, output_file: str) -> None:
    """Convert text to speech using pyttsx3 and save as MP3.

    Args:
        text: Text to convert.
        output_file: Path to output MP3 file.

    Raises:
        PermissionError: If output file cannot be written.
        Exception: If pyttsx3 fails.
    """
    logging.info("Converting text to speech with pyttsx3: %s", output_file)
    try:
        engine = pyttsx3.init()
        engine.save_to_file(text, output_file)
        engine.runAndWait()
        engine.stop()
        logging.info("MP3 file written: %s", output_file)
    except PermissionError as e:
        logging.error("Cannot write to output file %s: %s", output_file, e)
        raise
    except Exception as e:
        logging.error("pyttsx3 conversion failed: %s", e)
        raise


def main() -> int:
    """Main entry point for PdfToSpeech.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    args = parse_args()
    setup_logging(args.verbose, args.logfile)

    # Validate output file extension
    if not args.output_file.lower().endswith(".mp3"):
        logging.error("Output file must have .mp3 extension")
        return 1

    try:
        clean_text = extract_pdf_text(args.input_file)
        if not clean_text:
            logging.error("No text extracted from PDF")
            return 1

        if args.engine == "gtts":
            google_text_to_speech(clean_text, args.output_file)
        else:
            pyttsx3_text_to_speech(clean_text, args.output_file)
        return 0
    except KeyboardInterrupt:
        logging.info("Cancelled by user")
        return 0
    except Exception as e:
        logging.error("Error: %s", e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
