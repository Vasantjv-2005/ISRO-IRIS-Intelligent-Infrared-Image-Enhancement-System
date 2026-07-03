"""
Analysis Model

This model represents the AI analysis results generated
after processing an infrared image.
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


class AnalysisStatus(str, Enum):
    """
    Status of the AI analysis.
    """

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class DetectedObject(BaseModel):
    """
    Represents a detected object.
    """

    label: str
    confidence: float
    bounding_box: list[float]


class AnalysisModel(BaseModel):
    """
    Analysis document stored in MongoDB.
    """

    analysis_id: str = Field(default_factory=lambda: str(uuid4()))

    upload_id: str

    image_name: str | None = None

    status: AnalysisStatus = AnalysisStatus.PENDING

    scene_summary: str | None = None

    detailed_analysis: str | None = None

    detected_objects: list[DetectedObject] = Field(default_factory=list)

    object_count: int = 0

    confidence_score: float = 0.0

    report_generated: bool = False

    report_path: str | None = None

    analyzed_at: datetime | None = None

    created_at: datetime = Field(default_factory=utc_now)

    updated_at: datetime = Field(default_factory=utc_now)

    model_config = {
        "populate_by_name": True,
        "extra": "ignore",
        "validate_assignment": True,
    }