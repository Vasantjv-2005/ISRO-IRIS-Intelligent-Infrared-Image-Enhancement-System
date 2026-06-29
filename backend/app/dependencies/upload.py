"""
Upload Dependencies

Provides reusable Upload Service dependencies
for FastAPI.
"""

from app.services.upload.upload_service import (
    UploadService,
    upload_service,
)


def get_upload_service() -> UploadService:
    """
    Return the Upload Service instance.
    """

    return upload_service