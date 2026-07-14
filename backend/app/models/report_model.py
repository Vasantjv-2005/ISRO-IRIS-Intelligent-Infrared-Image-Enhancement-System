"""
Report Model

This model stores the generated report details
for an analyzed infrared image.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field, model_validator


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

    upload_id: str = ""

    analysis_id: str | None = ""

    status: ReportStatus = ReportStatus.PENDING

    report_title: str = ""

    report_path: str = ""

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

    @model_validator(mode="before")
    @classmethod
    def map_legacy_fields(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "report_title" not in data or data["report_title"] is None or not str(data["report_title"]).strip():
                data["report_title"] = data.get("title") or f"Comprehensive Dossier - {data.get('upload_id', 'IRIS')}"
            if "analysis_id" not in data or data["analysis_id"] is None:
                data["analysis_id"] = data.get("upload_id") or ""
            if "upload_id" not in data or data["upload_id"] is None:
                data["upload_id"] = ""
            if "report_path" not in data or data["report_path"] is None:
                data["report_path"] = f"reports/{data.get('report_id', '')}"
        return data

    model_config = {
        "populate_by_name": True,
        "extra": "ignore",
        "validate_assignment": True,
    }