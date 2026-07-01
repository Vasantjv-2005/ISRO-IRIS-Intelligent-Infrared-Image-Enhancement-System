"""
Tests for Upload API.
"""

from datetime import datetime
from io import BytesIO
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.models.upload_model import ProcessingStatus


client = TestClient(app)


# ==========================================================
# Successful Upload
# ==========================================================

@patch("app.api.routes.upload.upload_service.upload_image")
def test_upload_image_success(mock_upload: AsyncMock):
    """
    Test successful image upload.
    """

    mock_upload.return_value = {
        "upload_id": "upload_123",
        "filename": "thermal.jpg",
        "original_filename": "thermal.jpg",
        "file_path": "uploads/thermal.jpg",
        "file_size": 102400,
        "file_type": "jpg",
        "mime_type": "image/jpeg",
        "status": ProcessingStatus.UPLOADED,
        "uploaded_at": datetime.utcnow(),
        "message": "Image uploaded successfully.",
    }

    files = {
        "file": (
            "thermal.jpg",
            BytesIO(b"fake image"),
            "image/jpeg",
        )
    }

    response = client.post(
        "/upload/",
        files=files,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["upload_id"] == "upload_123"
    assert data["filename"] == "thermal.jpg"
    assert data["original_filename"] == "thermal.jpg"
    assert data["file_path"] == "uploads/thermal.jpg"
    assert data["file_size"] == 102400
    assert data["file_type"] == "jpg"
    assert data["mime_type"] == "image/jpeg"
    assert data["message"] == "Image uploaded successfully."

    mock_upload.assert_awaited_once()


# ==========================================================
# Missing File
# ==========================================================

def test_upload_without_file():
    """
    File is required.
    """

    response = client.post("/upload/")

    assert response.status_code == 422


# ==========================================================
# Invalid Content Type
# ==========================================================

@patch("app.api.routes.upload.upload_service.upload_image")
def test_upload_invalid_file(mock_upload: AsyncMock):
    """
    Upload a text file.
    """

    mock_upload.side_effect = ValueError(
        "Unsupported file type."
    )

    files = {
        "file": (
            "notes.txt",
            BytesIO(b"Hello"),
            "text/plain",
        )
    }

    response = client.post(
        "/upload/",
        files=files,
    )

    assert response.status_code in (
        400,
        422,
        500,
    )


# ==========================================================
# Empty File
# ==========================================================

@patch("app.api.routes.upload.upload_service.upload_image")
def test_empty_file(mock_upload: AsyncMock):
    """
    Upload an empty image.
    """

    mock_upload.side_effect = ValueError(
        "Empty file."
    )

    files = {
        "file": (
            "thermal.jpg",
            BytesIO(b""),
            "image/jpeg",
        )
    }

    response = client.post(
        "/upload/",
        files=files,
    )

    assert response.status_code in (
        400,
        422,
        500,
    )