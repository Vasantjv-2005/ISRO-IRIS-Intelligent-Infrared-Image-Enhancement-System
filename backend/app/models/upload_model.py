"""
Upload Model

This model defines the structure of an uploaded infrared image
stored in MongoDB.
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ProcessingStatus(str, Enum):
    """
    Status of the uploaded image.
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
    Upload document stored in MongoDB.
    """

    filename: str
    original_filename: str
    file_path: str
    file_size: int
    file_type: str

    status: ProcessingStatus = ProcessingStatus.UPLOADED

    uploaded_at: datetime = Field(default_factory=datetime.utcnow)

    enhancement_completed: bool = False
    colorization_completed: bool = False
    detection_completed: bool = False
    analysis_completed: bool = False
    report_generated: bool = False

    report_path: str | None = None

    objects_detected: list = Field(default_factory=list)

    scene_summary: str | None = None

    created_at: datetime = Field(default_factory=datetime.utcnow)

    updated_at: datetime = Field(default_factory=datetime.utcnow)