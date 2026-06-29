"""
Comparison Schemas

Request and response schemas for comparing
original and processed images.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ComparisonStatus(str, Enum):
    """
    Comparison processing status.
    """

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ComparisonRequestSchema(BaseModel):
    """
    Request schema for image comparison.
    """

    upload_id: str = Field(
        ...,
        description="Unique upload ID"
    )


class ComparisonResponseSchema(BaseModel):
    """
    Response schema for image comparison.
    """

    upload_id: str

    status: ComparisonStatus

    original_image_path: str

    processed_image_path: str

    comparison_image_path: Optional[str] = None

    enhancement_applied: bool = False

    colorization_applied: bool = False

    object_detection_applied: bool = False

    scene_analysis_applied: bool = False

    total_objects: int = 0

    similarity_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0
    )

    processing_time_seconds: float = Field(
        default=0.0,
        ge=0.0
    )

    created_at: Optional[datetime] = None


class ComparisonStatusResponse(BaseModel):
    """
    Current comparison status.
    """

    upload_id: str

    status: ComparisonStatus

    progress: int = Field(
        default=0,
        ge=0,
        le=100
    )

    message: str