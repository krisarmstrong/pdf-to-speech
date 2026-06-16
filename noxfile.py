"""Automation sessions for pdf-to-speech."""

from __future__ import annotations

import nox

nox.options.sessions = ["tests"]


@nox.session
def tests(session: nox.Session) -> None:
    """Run the test suite under the active interpreter."""
    # Runtime deps are absent from [project.dependencies] — install from requirements.txt.
    session.install("pypdf==6.13.2", "gTTS>=2.5.4,<3.0.0", "pyttsx3>=2.99,<3.0.0")
    session.install("-e", ".")
    session.install("pytest", "pytest-cov")
    session.run("pytest", "--cov=pdf_to_speech", "--cov-report=term-missing")
