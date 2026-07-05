"""
Configuration management.

Loads settings from environment variables.
Students should not need to modify this file.
"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

DEFAULT_GEMINI_MODEL = "gemini-2.0-flash"
SUPPORTED_GEMINI_MODELS = {
    "gemini-2.0-flash": "gemini-2.0-flash",
    "gemini-2.0-flash-lite": "gemini-2.0-flash-lite",
    "gemini-1.5-flash": "gemini-1.5-flash",
    "gemini-1.5-pro": "gemini-1.5-pro",
}


@dataclass
class Settings:
    """Application settings."""

    model_name: str = DEFAULT_GEMINI_MODEL
    google_api_key: Optional[str] = None
    google_credentials_path: Optional[Path] = None
    debug_mode: bool = False
    enable_retry: bool = True
    max_retries: int = 3
    retry_delay: float = 1.0
    calendar_max_results: int = 50
    gmail_max_results: int = 100
    sheets_max_rows: int = 1000

    def __init__(self):
        load_dotenv()

        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.model_name = self._normalize_model_name(
            os.getenv("MODEL_NAME", DEFAULT_GEMINI_MODEL)
        )
        creds_path = os.getenv("GOOGLE_CREDENTIALS_PATH")
        if creds_path:
            self.google_credentials_path = Path(creds_path)
        else:
            self.google_credentials_path = (
                Path(__file__).parent / "credentials" / "credentials.json"
            )

        self.debug_mode = os.getenv("DEBUG", "false").lower() == "true"
        self.enable_retry = os.getenv("ENABLE_RETRY", "true").lower() == "true"
        self.max_retries = int(os.getenv("MAX_RETRIES", "3"))
        self.retry_delay = float(os.getenv("RETRY_DELAY", "1.0"))
        self.calendar_max_results = int(os.getenv("CALENDAR_MAX_RESULTS", "50"))
        self.gmail_max_results = int(os.getenv("GMAIL_MAX_RESULTS", "100"))
        self.sheets_max_rows = int(os.getenv("SHEETS_MAX_ROWS", "1000"))

    def _normalize_model_name(self, model_name: str) -> str:
        """Normalize configured model names to supported ADK/Gemini identifiers."""
        if not model_name:
            return DEFAULT_GEMINI_MODEL

        normalized = model_name.strip().lower().replace(" ", "-")
        normalized = normalized.replace("_", "-")
        normalized = normalized.replace("‑", "-").replace("–", "-").replace("—", "-")
        normalized = "".join(ch for ch in normalized if ch.isalnum() or ch in "-._")

        if normalized in SUPPORTED_GEMINI_MODELS:
            return SUPPORTED_GEMINI_MODELS[normalized]

        if normalized.startswith("gemini"):
            return normalized

        return DEFAULT_GEMINI_MODEL

    def validate(self) -> bool:
        """Check if configuration is valid."""
        if not self.google_credentials_path.exists():
            print(f"Warning: Credentials not found at {self.google_credentials_path}")
            return False
        return True
