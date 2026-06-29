"""
Preprocessing Schemas

Request and response schemas for image preprocessing.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class PreprocessingStatus(str, Enum):
    """
    Image preprocessing status.
    """

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class PreprocessingRequestSchema(BaseModel):
    """
    Request schema for image preprocessing.
    """

    upload_id: str = Field(
        ...,
        description="Unique upload ID"
    )


class PreprocessingResponseSchema(BaseModel):
    """
    Response schema after preprocessing.
    """

    upload_id: str

    status: PreprocessingStatus

    original_image_path: str

    preprocessed_image_path: Optional[str] = None

    resized: bool = False

    normalized: bool = False

    noise_removed: bool = False

    contrast_enhanced: bool = False

    processing_time_seconds: float = Field(
        default=0.0,
        ge=0.0
    )

    preprocessing_completed: bool = False

    completed_at: Optional[datetime] = None


class PreprocessingStatusResponse(BaseModel):
    """
    Preprocessing progress response.
    """

    upload_id: str

    status: PreprocessingStatus

    progress: int = Field(
        default=0,
        ge=0,
        le=100
    )

    message: str