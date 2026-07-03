"""
Session Schemas

Request and response schemas for image processing sessions.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.session_model import SessionStatus


class SessionCreateRequest(BaseModel):
    """
    Request schema to create a new session.
    """

    upload_id: str = Field(..., description="ID of the uploaded image.")


class SessionResponseSchema(BaseModel):
    """
    Session details response schema.
    """

    session_id: str
    upload_id: str
    image_id: Optional[str] = None
    analysis_id: Optional[str] = None
    report_id: Optional[str] = None
    comparison_id: Optional[str] = None
    status: SessionStatus
    progress: int = Field(default=0, ge=0, le=100)
    current_stage: str = "Upload"
    started_at: datetime
    completed_at: Optional[datetime] = None
    processing_time_seconds: float = 0.0
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


class SessionStatusResponse(BaseModel):
    """
    Session processing status and progress response.
    """

    session_id: str
    status: SessionStatus
    progress: int = Field(default=0, ge=0, le=100)
    current_stage: str
    message: str


class SessionListResponse(BaseModel):
    """
    Paginated or limited list of sessions.
    """

    total_sessions: int
    sessions: list[SessionResponseSchema]