"""
Upload Model

Defines the MongoDB document structure for uploaded
infrared images.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


def utc_now() -> datetime:
    """
    Return the current UTC datetime.
    """

    return datetime.now(timezone.utc)


class ProcessingStatus(str, Enum):
    """
    Processing status of an uploaded image.
    """

    UPLOADED = "uploaded"
    PREPROCESSING = "preprocessing"
    ENHANCED = "enhanced"
    COLORIZED = "colorized"
    DETECTED = "detected"
    ANALYZED = "analyzed"
    COMPLETED = "completed"
    FAILED = "failed"


class UploadModel(BaseModel):
    """
    MongoDB Upload Document.
    """

    # =====================================================
    # Identification
    # =====================================================

    upload_id: str

    # =====================================================
    # File Information
    # =====================================================

    filename: str

    original_filename: str

    file_path: str

    file_size: int

    file_type: str

    mime_type: str

    # =====================================================
    # Processing
    # =====================================================

    status: ProcessingStatus = ProcessingStatus.UPLOADED

    uploaded_at: datetime = Field(default_factory=utc_now)

    preprocessing_completed: bool = False

    enhancement_completed: bool = False

    colorization_completed: bool = False

    detection_completed: bool = False

    analysis_completed: bool = False

    report_generated: bool = False

    # =====================================================
    # AI Results & Stage Paths
    # =====================================================

    preprocessed_path: str | None = None

    enhanced_path: str | None = None

    colorized_path: str | None = None

    detected_path: str | None = None

    analyzed_path: str | None = None

    report_path: str | None = None

    objects_detected: list[dict] = Field(
        default_factory=list
    )

    scene_summary: str | None = None

    # =====================================================
    # Audit Fields
    # =====================================================

    created_at: datetime = Field(
        default_factory=utc_now
    )

    updated_at: datetime = Field(
        default_factory=utc_now
    )

    model_config = {
        "populate_by_name": True,
        "extra": "ignore",
        "validate_assignment": True,
    }