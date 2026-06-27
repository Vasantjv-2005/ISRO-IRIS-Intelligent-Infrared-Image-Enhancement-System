"""
Comparison Model

This model stores the comparison details between
the original infrared image and the AI-processed image.
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ComparisonStatus(str, Enum):
    """
    Status of image comparison.
    """

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ComparisonModel(BaseModel):
    """
    Comparison document stored in MongoDB.
    """

    upload_id: str

    original_image_path: str

    processed_image_path: str

    comparison_image_path: str | None = None

    status: ComparisonStatus = ComparisonStatus.PENDING

    enhancement_applied: bool = False

    colorization_applied: bool = False

    object_detection_applied: bool = False

    scene_analysis_applied: bool = False

    detected_objects: list[str] = Field(default_factory=list)

    total_objects: int = 0

    ai_summary: str | None = None

    processing_time_seconds: float = 0.0

    similarity_score: float = 0.0

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)