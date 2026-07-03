"""
Report Model

This model stores the generated report details
for an analyzed infrared image.
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

    report_id: str = Field(default_factory=lambda: str(uuid4()))

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

    created_at: datetime = Field(default_factory=utc_now)

    updated_at: datetime = Field(default_factory=utc_now)

    model_config = {
        "populate_by_name": True,
        "extra": "ignore",
        "validate_assignment": True,
    }