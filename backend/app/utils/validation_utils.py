"""
Validation Utilities

Reusable validation helper functions for the
IRIS Backend.
"""

from __future__ import annotations

import re
from pathlib import Path


class ValidationUtils:
    """
    Utility class for validating files,
    images, strings and numbers.
    """

    ALLOWED_IMAGE_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".tif",
        ".tiff",
        ".webp",
    }

    # =====================================================
    # Image Extension
    # =====================================================

    @staticmethod
    def is_valid_image_extension(
        filename: str,
    ) -> bool:
        """
        Validate image extension.
        """

        extension = Path(filename).suffix.lower()

        return extension in ValidationUtils.ALLOWED_IMAGE_EXTENSIONS

    # =====================================================
    # File Exists
    # =====================================================

    @staticmethod
    def file_exists(
        path: str,
    ) -> bool:
        """
        Check whether a file exists.
        """

        return Path(path).is_file()

    # =====================================================
    # Directory Exists
    # =====================================================

    @staticmethod
    def directory_exists(
        path: str,
    ) -> bool:
        """
        Check whether a directory exists.
        """

        return Path(path).is_dir()

    # =====================================================
    # Confidence
    # =====================================================

    @staticmethod
    def is_valid_confidence(
        confidence: float,
    ) -> bool:
        """
        Confidence must be between 0 and 1.
        """

        return 0.0 <= confidence <= 1.0

    # =====================================================
    # Progress
    # =====================================================

    @staticmethod
    def is_valid_progress(
        progress: int,
    ) -> bool:
        """
        Progress must be between 0 and 100.
        """

        return 0 <= progress <= 100

    # =====================================================
    # Positive Integer
    # =====================================================

    @staticmethod
    def is_positive_integer(
        value: int,
    ) -> bool:
        """
        Validate positive integer.
        """

        return value > 0

    # =====================================================
    # Positive Number
    # =====================================================

    @staticmethod
    def is_positive_number(
        value: float,
    ) -> bool:
        """
        Validate positive number.
        """

        return value > 0

    # =====================================================
    # Email
    # =====================================================

    @staticmethod
    def is_valid_email(
        email: str,
    ) -> bool:
        """
        Validate email format.
        """

        pattern = (
            r"^[A-Za-z0-9._%+-]+@"
            r"[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        )

        return re.fullmatch(
            pattern,
            email,
        ) is not None

    # =====================================================
    # Empty String
    # =====================================================

    @staticmethod
    def is_not_empty(
        value: str,
    ) -> bool:
        """
        Validate non-empty string.
        """

        return bool(value.strip())

    # =====================================================
    # Image Path
    # =====================================================

    @staticmethod
    def validate_image_path(
        image_path: str,
    ) -> bool:
        """
        Validate image file.
        """

        path = Path(image_path)

        return (
            path.exists()
            and path.is_file()
            and ValidationUtils.is_valid_image_extension(
                path.name
            )
        )

    # =====================================================
    # File Size
    # =====================================================

    @staticmethod
    def validate_file_size(
        file_size: int,
        max_size_mb: int = 20,
    ) -> bool:
        """
        Validate maximum file size.
        """

        return file_size <= max_size_mb * 1024 * 1024

    # =====================================================
    # Path Safety
    # =====================================================

    @staticmethod
    def is_safe_path(
        path: str,
    ) -> bool:
        """
        Prevent simple directory traversal.
        """

        return ".." not in Path(path).parts


validation_utils = ValidationUtils()