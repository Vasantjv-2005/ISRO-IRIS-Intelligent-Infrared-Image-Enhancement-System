"""
Image Storage Service

Handles saving, retrieving, and deleting image files
for the IRIS Backend.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.settings import settings


class ImageStorageService:
    """
    Service responsible for image storage operations.
    """

    def __init__(self) -> None:
        self.raw_directory = Path(settings.UPLOAD_FOLDER)

        self.raw_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    async def save_image(
        self,
        file: UploadFile,
    ) -> tuple[str, str]:
        """
        Save an uploaded image.

        Returns:
            tuple(original_filename, stored_file_path)
        """

        extension = Path(file.filename).suffix.lower()

        unique_filename = f"{uuid4().hex}{extension}"

        destination = self.raw_directory / unique_filename

        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return (
            file.filename,
            str(destination),
        )

    def image_exists(
        self,
        image_path: str,
    ) -> bool:
        """
        Check whether an image exists.
        """

        return Path(image_path).exists()

    def delete_image(
        self,
        image_path: str,
    ) -> bool:
        """
        Delete an image from storage.
        """

        path = Path(image_path)

        if not path.exists():
            return False

        path.unlink()

        return True

    def create_directory(
        self,
        directory: str,
    ) -> None:
        """
        Create a directory if it does not exist.
        """

        Path(directory).mkdir(
            parents=True,
            exist_ok=True,
        )

    def get_image_path(
        self,
        filename: str,
    ) -> str:
        """
        Return the absolute image path.
        """

        return str(
            self.raw_directory / filename
        )


image_storage = ImageStorageService()