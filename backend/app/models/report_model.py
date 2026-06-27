"""
Report Model

This model stores the generated report details
for an analyzed infrared image.
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ReportStatus(str, Enum):
    """
    Status of report generation.
    """

    PENDING = "pending"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


class ReportModel(BaseModel):
    """
    Report document stored in MongoDB.
    """

    upload_id: str

    analysis_id: str

    status: ReportStatus = ReportStatus.PENDING

    report_title: str

    report_path: str

    report_format: str = "pdf"

    report_size: int = 0

    generated_by: str = "IRIS AI"

    ai_summary: str | None = None

    total_objects_detected: int = 0

    detected_objects: list[str] = Field(default_factory=list)

    confidence_score: float = 0.0

    download_count: int = 0

    generated_at: datetime | None = None

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)