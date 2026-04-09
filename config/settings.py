"""
Global application configuration.

All environment-specific settings are read from environment variables
with sensible defaults so the application can run without a .env file.
"""

import os


class Config:
    # Flask
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "change-me-in-production")
    DEBUG: bool = os.environ.get("DEBUG", "True").lower() == "true"

    # CSRF
    WTF_CSRF_ENABLED: bool = True

    # File export
    EXPORT_MAX_ROWS: int = int(os.environ.get("EXPORT_MAX_ROWS", "200"))
