"""
Dashboard Schemas

Request and response schemas for the IRIS Dashboard.
"""

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class DashboardStatisticsSchema(BaseModel):
    """
    Dashboard statistics.
    """

    total_uploads: int = 0

    total_processed_images: int = 0

    total_reports_generated: int = 0

    total_objects_detected: int = 0

    total_completed_analysis: int = 0

    total_failed_jobs: int = 0

    active_sessions: int = 0

    processing_success_rate: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0
    )

    average_processing_time_seconds: float = Field(
        default=0.0,
        ge=0.0
    )

    storage_used_mb: float = Field(
        default=0.0,
        ge=0.0
    )


class RecentActivitySchema(BaseModel):
    """
    Recent dashboard activity.
    """

    upload_id: str

    filename: str

    status: str

    uploaded_at: datetime


class SystemHealthSchema(BaseModel):
    """
    System health information.
    """

    backend_status: str = "Online"

    database_status: str = "Connected"

    ai_model_status: str = "Ready"

    uptime: str = "0h 0m"

    last_updated: datetime


class DashboardResponseSchema(BaseModel):
    """
    Complete dashboard response.
    """

    statistics: DashboardStatisticsSchema

    recent_activities: List[RecentActivitySchema] = Field(
        default_factory=list
    )

    system_health: SystemHealthSchema