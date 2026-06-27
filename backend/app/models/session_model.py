"""
Session Model

Stores information about an image processing session.
Each uploaded image belongs to one processing session.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


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

    session_id: str

    upload_id: str

    image_id: Optional[str] = None

    analysis_id: Optional[str] = None

    report_id: Optional[str] = None

    comparison_id: Optional[str] = None

    status: SessionStatus = SessionStatus.CREATED

    progress: int = 0

    current_stage: str = "Upload"

    started_at: datetime = Field(default_factory=datetime.utcnow)

    completed_at: Optional[datetime] = None

    processing_time_seconds: float = 0.0

    error_message: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)