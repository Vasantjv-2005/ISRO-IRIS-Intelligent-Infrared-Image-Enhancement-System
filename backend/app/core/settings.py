"""
Application Settings

Loads and validates all environment variables
required by the IRIS Backend.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from the .env file.
    """

    # =====================================================
    # Project Information
    # =====================================================

    PROJECT_NAME: str = "IRIS"

    PROJECT_DESCRIPTION: str = (
        "Intelligent Infrared Image Enhancement & Interpretation System"
    )

    PROJECT_VERSION: str = "1.0.0"

    # =====================================================
    # API
    # =====================================================

    API_PREFIX: str = "/api"

    # =====================================================
    # Server
    # =====================================================

    HOST: str = "127.0.0.1"

    PORT: int = 8000

    DEBUG: bool = True

    # =====================================================
    # MongoDB
    # =====================================================

    MONGODB_URI: str = Field(...)

    DATABASE_NAME: str = Field(...)

    # =====================================================
    # Gemini
    # =====================================================

    GEMINI_API_KEY: str = Field(...)

    # =====================================================
    # Upload Settings
    # =====================================================

    MAX_FILE_SIZE: int = 20 * 1024 * 1024

    ALLOWED_IMAGE_TYPES: list[str] = [
        "image/png",
        "image/jpeg",
        "image/jpg",
        "image/tiff",
    ]

    # =====================================================
    # Image Storage
    # =====================================================

    UPLOAD_FOLDER: str = "uploads/raw"

    OUTPUT_FOLDER: str = "outputs"

    # =====================================================
    # AI Models
    # =====================================================

    YOLO_MODEL_PATH: str = "weights/yolov8.pt"

    # =====================================================
    # Environment Configuration
    # =====================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Returns a cached instance of the application settings.
    """

    return Settings()


settings = get_settings()