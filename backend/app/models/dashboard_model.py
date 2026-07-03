"""
Dashboard Model

Stores dashboard statistics and system information
for the IRIS application.
"""

from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field


def utc_now() -> datetime:
    """
    Return the current UTC datetime.
    """

    return datetime.now(timezone.utc)


class DashboardModel(BaseModel):
    """
    Dashboard statistics model.
    """

    dashboard_id: str = Field(default="stats")

    total_uploads: int = 0

    total_processed_images: int = 0

    total_reports_generated: int = 0

    total_objects_detected: int = 0

    total_completed_analysis: int = 0

    total_failed_jobs: int = 0

    processing_success_rate: float = 0.0

    average_processing_time_seconds: float = 0.0

    storage_used_mb: float = 0.0

    system_status: str = "Online"

    active_sessions: int = 0

    created_at: datetime = Field(default_factory=utc_now)

    updated_at: datetime = Field(default_factory=utc_now)

    model_config = {
        "populate_by_name": True,
        "extra": "ignore",
        "validate_assignment": True,
    }