"""
Upload Validation Service

Validates uploaded image files before they are
stored or processed.
"""

from pathlib import Path

from fastapi import UploadFile

from app.core.settings import settings
from app.middleware.error_handler import (
    FileUploadException,
    ValidationException,
)


class ValidationService:
    """
    Service responsible for validating uploaded files.
    """

    @staticmethod
    def validate_filename(file: UploadFile) -> None:
        """
        Validate the uploaded filename.
        """

        if not file.filename:
            raise ValidationException("Filename is missing.")

        if len(file.filename.strip()) == 0:
            raise ValidationException("Filename cannot be empty.")

    @staticmethod
    def validate_extension(file: UploadFile) -> None:
        """
        Validate the file extension.
        """

        allowed_extensions = {
            ".png",
            ".jpg",
            ".jpeg",
            ".tif",
            ".tiff",
            "image/x-tiff",
        }

        extension = Path(file.filename).suffix.lower()

        if extension not in allowed_extensions:
            raise FileUploadException(
                "Only PNG, JPG, JPEG and TIFF images are supported."
            )

    @staticmethod
    def validate_content_type(file: UploadFile) -> None:
        """
        Validate the MIME type.
        """

        if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
            raise FileUploadException(
                "Unsupported image content type."
            )

    @staticmethod
    async def validate_file_size(file: UploadFile) -> None:
        """
        Validate uploaded file size.
        """

        contents = await file.read()

        size = len(contents)

        await file.seek(0)

        if size > settings.MAX_FILE_SIZE:
            raise FileUploadException(
                f"Maximum allowed file size is "
                f"{settings.MAX_FILE_SIZE // (1024 * 1024)} MB."
            )

    @classmethod
    async def validate(cls, file: UploadFile) -> None:
        """
        Run all upload validations.
        """

        cls.validate_filename(file)

        cls.validate_extension(file)

        cls.validate_content_type(file)

        await cls.validate_file_size(file)


validation_service = ValidationService()