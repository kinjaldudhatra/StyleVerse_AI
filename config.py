import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from a local .env file when it exists.
load_dotenv(BASE_DIR / ".env")


class Config:
    """Application settings loaded from environment variables."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-secret-key")
    DEBUG = os.environ.get("FLASK_DEBUG", "1") == "1"
    DATABASE_PATH = BASE_DIR / "database" / "fashion.db"

    VTON_SERVICE_URL = os.environ.get(
        "VTON_SERVICE_URL",
        "http://127.0.0.1:5055"
    )

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
