"""
Analysis Schemas

Request and response schemas for AI image analysis.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class AnalysisStatus(str, Enum):
    """
    Analysis processing status.
    """

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class DetectedObjectSchema(BaseModel):
    """
    Detected object information.
    """

    label: str = Field(..., description="Detected object name")
    confidence: float = Field(..., ge=0.0, le=1.0)
    bounding_box: List[float] = Field(
        ...,
        description="Bounding box [x1, y1, x2, y2]"
    )


class AnalysisRequestSchema(BaseModel):
    """
    Request for image analysis.
    """

    upload_id: str


class AnalysisResponseSchema(BaseModel):
    """
    Complete AI analysis response.
    """

    upload_id: str

    status: AnalysisStatus

    scene_summary: Optional[str] = None

    detailed_analysis: Optional[str] = None

    detected_objects: List[DetectedObjectSchema] = Field(default_factory=list)

    object_count: int = 0

    confidence_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0
    )

    report_generated: bool = False

    report_path: Optional[str] = None

    analyzed_at: Optional[datetime] = None


class AnalysisStatusResponse(BaseModel):
    """
    Analysis status response.
    """

    upload_id: str

    status: AnalysisStatus

    progress: int = Field(
        default=0,
        ge=0,
        le=100
    )

    message: str