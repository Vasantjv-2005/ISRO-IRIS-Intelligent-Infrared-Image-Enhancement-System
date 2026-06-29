"""
Colorization Schemas

Request and response schemas for AI image colorization.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ColorizationStatus(str, Enum):
    """
    Colorization processing status.
    """

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ColorizationRequestSchema(BaseModel):
    """
    Request schema for image colorization.
    """

    upload_id: str = Field(
        ...,
        description="Unique upload ID"
    )


class ColorizationResponseSchema(BaseModel):
    """
    Response schema after image colorization.
    """

    upload_id: str

    status: ColorizationStatus

    original_image_path: str

    colorized_image_path: Optional[str] = None

    processing_time_seconds: float = Field(
        default=0.0,
        ge=0.0
    )

    model_name: str = "AIDC-AI/Ours_EnhanceAndColorization"

    colorization_completed: bool = False

    completed_at: Optional[datetime] = None


class ColorizationStatusResponse(BaseModel):
    """
    Current colorization status.
    """

    upload_id: str

    status: ColorizationStatus

    progress: int = Field(
        default=0,
        ge=0,
        le=100
    )

    message: str