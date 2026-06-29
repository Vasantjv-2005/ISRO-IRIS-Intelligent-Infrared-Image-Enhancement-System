"""
Enhancement Schemas

Request and response schemas for AI image enhancement.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class EnhancementStatus(str, Enum):
    """
    Image enhancement status.
    """

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class EnhancementRequestSchema(BaseModel):
    """
    Request schema for image enhancement.
    """

    upload_id: str = Field(
        ...,
        description="Unique upload ID"
    )


class EnhancementResponseSchema(BaseModel):
    """
    Response schema after image enhancement.
    """

    upload_id: str

    status: EnhancementStatus

    original_image_path: str

    enhanced_image_path: Optional[str] = None

    model_name: str = "IRIS Enhancement Model"

    brightness_improved: bool = False

    contrast_improved: bool = False

    noise_reduced: bool = False

    sharpness_improved: bool = False

    processing_time_seconds: float = Field(
        default=0.0,
        ge=0.0
    )

    enhancement_completed: bool = False

    completed_at: Optional[datetime] = None


class EnhancementStatusResponse(BaseModel):
    """
    Enhancement progress response.
    """

    upload_id: str

    status: EnhancementStatus

    progress: int = Field(
        default=0,
        ge=0,
        le=100
    )

    message: str