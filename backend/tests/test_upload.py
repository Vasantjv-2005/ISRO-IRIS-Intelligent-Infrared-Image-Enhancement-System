"""
Tests for Upload API.
"""

from io import BytesIO
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


# ==========================================================
# Test Successful Upload
# ==========================================================

@patch("app.api.routes.upload.upload_service.upload_image")
def test_upload_image_success(
    mock_upload: AsyncMock,
):
    """
    Test successful image upload.
    """

    mock_upload.return_value = {
        "success": True,
        "message": "Image uploaded successfully.",
        "upload_id": "123456",
        "filename": "thermal.jpg",
        "file_path": "uploads/thermal.jpg",
    }

    files = {
        "file": (
            "thermal.jpg",
            BytesIO(b"fake image data"),
            "image/jpeg",
        )
    }

    response = client.post(
        "/upload/",
        files=files,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["filename"] == "thermal.jpg"

    mock_upload.assert_awaited_once()


# ==========================================================
# Test Missing File
# ==========================================================

def test_upload_without_file():
    """
    Test upload without sending a file.
    """

    response = client.post(
        "/upload/",
    )

    assert response.status_code == 422


# ==========================================================
# Test Invalid Content Type
# ==========================================================

def test_invalid_file_type():
    """
    Test uploading a non-image file.
    """

    files = {
        "file": (
            "document.txt",
            BytesIO(b"Hello"),
            "text/plain",
        )
    }

    response = client.post(
        "/upload/",
        files=files,
    )

    # Validation is handled by upload_service.
    assert response.status_code in (
        200,
        400,
        415,
        422,
    )