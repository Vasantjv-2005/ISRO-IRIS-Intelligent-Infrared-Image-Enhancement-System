"""
Image Storage Service

Handles saving, retrieving, and deleting image files
for the IRIS Backend.
"""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.settings import settings


class ImageStorageService:
    """
    Service responsible for image storage operations.
    """

    def __init__(self) -> None:
        """
        Initialize all storage directories.
        """

        self.raw_directory = Path(settings.UPLOAD_FOLDER)
        self.preprocessed_directory = Path(settings.PREPROCESSED_FOLDER)
        self.enhanced_directory = Path(settings.ENHANCED_FOLDER)
        self.colorized_directory = Path(settings.COLORIZED_FOLDER)
        self.detected_directory = Path(settings.DETECTION_FOLDER)
        self.report_directory = Path(settings.REPORT_FOLDER)
        self.temp_directory = Path(settings.TEMP_FOLDER)

        self._create_directories()

    def _create_directories(self) -> None:
        """
        Create all required storage directories.
        """

        directories = [
            self.raw_directory,
            self.preprocessed_directory,
            self.enhanced_directory,
            self.colorized_directory,
            self.detected_directory,
            self.report_directory,
            self.temp_directory,
        ]

        for directory in directories:
            directory.mkdir(
                parents=True,
                exist_ok=True,
            )

    async def save_image(
        self,
        file: UploadFile,
    ) -> tuple[str, str, str, int, str]:
        """
        Save an uploaded image.

        Returns:
            (
                original_filename,
                stored_filename,
                stored_file_path,
                file_size,
                mime_type,
            )
        """

        extension = Path(file.filename).suffix.lower()

        stored_filename = f"{uuid4().hex}{extension}"

        destination = self.raw_directory / stored_filename

        contents = await file.read()

        with destination.open("wb") as buffer:
            buffer.write(contents)

        await file.seek(0)

        return (
            file.filename,
            stored_filename,
            str(destination),
            len(contents),
            file.content_type,
        )

    def image_exists(
        self,
        image_path: str,
    ) -> bool:
        """
        Check whether an image exists.
        """

        return Path(image_path).is_file()

    def delete_image(
        self,
        image_path: str,
    ) -> bool:
        """
        Delete an image from storage.
        """

        path = Path(image_path)

        if not path.is_file():
            return False

        path.unlink()

        return True

    def get_image_path(
        self,
        filename: str,
    ) -> str:
        """
        Return the full path of an image stored
        in the raw uploads directory.
        """

        return str(self.raw_directory / filename)

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


image_storage = ImageStorageService()