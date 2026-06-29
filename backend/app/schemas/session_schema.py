"""
Image Schemas

Request and response schemas for image information.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ImageStatus(str, Enum):
    """
    Image processing status.
    """

    UPLOADED = "uploaded"
    PREPROCESSED = "preprocessed"
    ENHANCED = "enhanced"
    COLORIZED = "colorized"
    DETECTED = "detected"
    ANALYZED = "analyzed"
    COMPLETED = "completed"
    FAILED = "failed"


class ImageMetadataSchema(BaseModel):
    """
    Image metadata.
    """

    width: int = Field(..., gt=0)

    height: int = Field(..., gt=0)

    format: str

    size: int = Field(..., gt=0)

    mime_type: str


class ImageResponseSchema(BaseModel):
    """
    Image response schema.
    """

    image_id: str

    upload_id: str

    original_filename: str

    stored_filename: str

    original_image_path: str

    processed_image_path: Optional[str] = None

    thumbnail_path: Optional[str] = None

    metadata: ImageMetadataSchema

    status: ImageStatus

    preprocessing_completed: bool = False

    enhancement_completed: bool = False

    colorization_completed: bool = False

    detection_completed: bool = False

    analysis_completed: bool = False

    report_generated: bool = False

    created_at: datetime

    updated_at: datetime


class ImageStatusResponse(BaseModel):
    """
    Image processing status.
    """

    image_id: str

    status: ImageStatus

    progress: int = Field(
        default=0,
        ge=0,
        le=100
    )

    message: str


class ImageDeleteResponse(BaseModel):
    """
    Image delete response.
    """

    image_id: str

    deleted: bool

    message: str


class ImageDownloadResponse(BaseModel):
    """
    Download processed image.
    """

    image_id: str

    file_name: str

    download_url: str