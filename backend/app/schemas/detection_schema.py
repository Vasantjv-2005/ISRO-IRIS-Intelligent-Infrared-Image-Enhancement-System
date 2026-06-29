"""
Detection Schemas

Request and response schemas for AI object detection.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class DetectionStatus(str, Enum):
    """
    Object detection status.
    """

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class BoundingBoxSchema(BaseModel):
    """
    Bounding box coordinates.
    """

    x_min: float = Field(..., ge=0.0)
    y_min: float = Field(..., ge=0.0)
    x_max: float = Field(..., ge=0.0)
    y_max: float = Field(..., ge=0.0)


class DetectedObjectSchema(BaseModel):
    """
    Information about a detected object.
    """

    class_name: str

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0
    )

    bounding_box: BoundingBoxSchema


class DetectionRequestSchema(BaseModel):
    """
    Request schema for object detection.
    """

    upload_id: str = Field(
        ...,
        description="Unique upload ID"
    )


class DetectionResponseSchema(BaseModel):
    """
    Object detection response.
    """

    upload_id: str

    status: DetectionStatus

    model_name: str = "YOLOv8"

    total_objects: int = 0

    detected_objects: List[DetectedObjectSchema] = Field(
        default_factory=list
    )

    annotated_image_path: Optional[str] = None

    processing_time_seconds: float = Field(
        default=0.0,
        ge=0.0
    )

    completed_at: Optional[datetime] = None


class DetectionStatusResponse(BaseModel):
    """
    Detection progress response.
    """

    upload_id: str

    status: DetectionStatus

    progress: int = Field(
        default=0,
        ge=0,
        le=100
    )

    message: str