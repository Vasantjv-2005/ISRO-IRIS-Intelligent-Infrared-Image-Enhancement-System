"""
Report Schemas

Request and response schemas for AI report generation.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class ReportStatus(str, Enum):
    """
    Report generation status.
    """

    PENDING = "pending"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


class ReportRequestSchema(BaseModel):
    """
    Request schema for report generation.
    """

    upload_id: str = Field(
        ...,
        description="Unique upload ID"
    )


class ReportResponseSchema(BaseModel):
    """
    Response schema after report generation.
    """

    upload_id: str

    report_title: str

    status: ReportStatus

    report_path: str

    report_format: str = "pdf"

    report_size: int = 0

    generated_by: str = "IRIS AI"

    ai_summary: Optional[str] = None

    total_objects_detected: int = 0

    detected_objects: List[str] = Field(default_factory=list)

    confidence_score: float = Field(
        default=0.0,
        ge=0.0,
        le=1.0
    )

    processing_time_seconds: float = Field(
        default=0.0,
        ge=0.0
    )

    generated_at: Optional[datetime] = None


class ReportDownloadSchema(BaseModel):
    """
    Report download response.
    """

    upload_id: str

    report_path: str

    download_url: str

    file_name: str


class ReportStatusResponse(BaseModel):
    """
    Report generation status.
    """

    upload_id: str

    status: ReportStatus

    progress: int = Field(
        default=0,
        ge=0,
        le=100
    )

    message: str