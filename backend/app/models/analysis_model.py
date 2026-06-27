"""
Analysis Model

This model represents the AI analysis results generated
after processing an infrared image.
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


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

    upload_id: str

    status: AnalysisStatus = AnalysisStatus.PENDING

    scene_summary: str | None = None

    detailed_analysis: str | None = None

    detected_objects: list[DetectedObject] = Field(default_factory=list)

    object_count: int = 0

    confidence_score: float = 0.0

    report_generated: bool = False

    report_path: str | None = None

    analyzed_at: datetime | None = None

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)