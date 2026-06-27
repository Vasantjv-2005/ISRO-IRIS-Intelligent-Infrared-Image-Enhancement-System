"""
Image Model

Represents an image processed by the IRIS pipeline.
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


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

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)