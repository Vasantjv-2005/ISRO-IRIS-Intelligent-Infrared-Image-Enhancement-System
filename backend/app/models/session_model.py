"""
Session Model

Stores information about an image processing session.
Each uploaded image belongs to one processing session.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


def utc_now() -> datetime:
    """
    Return the current UTC datetime.
    """

    return datetime.now(timezone.utc)


class SessionStatus(str, Enum):
    """
    Current status of the processing session.
    """

    CREATED = "created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class SessionModel(BaseModel):
    """
    Session document stored in MongoDB.
    """

    session_id: str = Field(default_factory=lambda: str(uuid4()))

    upload_id: str

    image_id: Optional[str] = None

    analysis_id: Optional[str] = None

    report_id: Optional[str] = None

    comparison_id: Optional[str] = None

    status: SessionStatus = SessionStatus.CREATED

    progress: int = 0

    current_stage: str = "Upload"

    started_at: datetime = Field(default_factory=utc_now)

    completed_at: Optional[datetime] = None

    processing_time_seconds: float = 0.0

    error_message: Optional[str] = None

    created_at: datetime = Field(default_factory=utc_now)

    updated_at: datetime = Field(default_factory=utc_now)

    model_config = {
        "populate_by_name": True,
        "extra": "ignore",
        "validate_assignment": True,
    }