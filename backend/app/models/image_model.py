"""
Image Model

Represents an image processed by the IRIS pipeline.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


def utc_now() -> datetime:
    """
    Return the current UTC datetime.
    """

    return datetime.now(timezone.utc)


class ImageStatus(str, Enum):
    """
    Processing status of an image.
    """

    UPLOADED = "uploaded"
    PREPROCESSED = "preprocessed"
    ENHANCED = "enhanced"
    COLORIZED = "colorized"
    DETECTED = "detected"
    ANALYZED = "analyzed"
    COMPLETED = "completed"
    FAILED = "failed"


class ImageModel(BaseModel):
    """
    Image document stored in MongoDB.
    """

    image_id: str = Field(default_factory=lambda: str(uuid4()))

    upload_id: str

    original_filename: str

    stored_filename: str

    original_image_path: str

    processed_image_path: str | None = None

    thumbnail_path: str | None = None

    image_width: int

    image_height: int

    image_format: str

    image_size: int

    mime_type: str

    status: ImageStatus = ImageStatus.UPLOADED

    preprocessing_completed: bool = False

    enhancement_completed: bool = False

    colorization_completed: bool = False

    detection_completed: bool = False

    analysis_completed: bool = False

    report_generated: bool = False

    created_at: datetime = Field(default_factory=utc_now)

    updated_at: datetime = Field(default_factory=utc_now)

    model_config = {
        "populate_by_name": True,
        "extra": "ignore",
        "validate_assignment": True,
    }