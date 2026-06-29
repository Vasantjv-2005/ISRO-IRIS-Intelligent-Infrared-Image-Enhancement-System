"""
Upload Schemas

Request and response schemas for image uploads.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class UploadStatus(str, Enum):
    """
    Upload status.
    """

    PENDING = "pending"
    UPLOADING = "uploading"
    COMPLETED = "completed"
    FAILED = "failed"


class UploadRequestSchema(BaseModel):
    """
    Upload request.
    """

    filename: str = Field(
        ...,
        min_length=1,
        max_length=255
    )

    file_size: int = Field(
        ...,
        gt=0
    )

    file_type: str

    mime_type: str


class UploadResponseSchema(BaseModel):
    """
    Upload response.
    """

    upload_id: str

    filename: str

    original_filename: str

    file_path: str

    file_size: int

    file_type: str

    mime_type: str

    status: UploadStatus

    uploaded_at: datetime

    message: str = "Image uploaded successfully."


class UploadStatusResponse(BaseModel):
    """
    Upload status response.
    """

    upload_id: str

    status: UploadStatus

    progress: int = Field(
        default=0,
        ge=0,
        le=100
    )

    message: str


class UploadDeleteResponse(BaseModel):
    """
    Delete upload response.
    """

    upload_id: str

    deleted: bool

    message: str


class UploadListItem(BaseModel):
    """
    Single uploaded image.
    """

    upload_id: str

    filename: str

    status: UploadStatus

    uploaded_at: datetime


class UploadListResponse(BaseModel):
    """
    Upload history.
    """

    total_uploads: int

    uploads: list[UploadListItem]