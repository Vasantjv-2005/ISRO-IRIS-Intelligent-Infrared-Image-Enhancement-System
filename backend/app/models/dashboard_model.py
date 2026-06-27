"""
Dashboard Model

Stores dashboard statistics and system information
for the IRIS application.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class DashboardModel(BaseModel):
    """
    Dashboard statistics model.
    """

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

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)