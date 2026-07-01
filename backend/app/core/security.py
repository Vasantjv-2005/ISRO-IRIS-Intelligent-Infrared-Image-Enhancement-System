"""
Security Utilities

Provides security-related helper functions
used throughout the IRIS Backend.
"""

from __future__ import annotations

import hashlib
import secrets
from pathlib import Path

from fastapi import HTTPException, UploadFile, status


class SecurityManager:
    """
    Security helper class.
    """

    # =====================================================
    # Generate Secure Token
    # =====================================================

    @staticmethod
    def generate_token(
        length: int = 32,
    ) -> str:
        """
        Generate a cryptographically secure token.
        """

        return secrets.token_hex(length)

    # =====================================================
    # Generate File Hash
    # =====================================================

    @staticmethod
    def generate_file_hash(
        file_path: str,
    ) -> str:
        """
        Generate SHA256 hash for a file.
        """

        sha256 = hashlib.sha256()

        with open(file_path, "rb") as file:

            while True:

                chunk = file.read(4096)

                if not chunk:
                    break

                sha256.update(chunk)

        return sha256.hexdigest()

    # =====================================================
    # Validate Image Extension
    # =====================================================

    @staticmethod
    def validate_image_extension(
        filename: str,
    ) -> bool:
        """
        Validate image extension.
        """

        allowed_extensions = {
            ".jpg",
            ".jpeg",
            ".png",
            ".bmp",
            ".tif",
            ".tiff",
            ".webp",
        }

        extension = Path(filename).suffix.lower()

        return extension in allowed_extensions

    # =====================================================
    # Validate Upload
    # =====================================================

    @staticmethod
    async def validate_upload(
        file: UploadFile,
        max_size_mb: int = 20,
    ) -> None:
        """
        Validate uploaded image.
        """

        if not SecurityManager.validate_image_extension(
            file.filename
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported image format.",
            )

        contents = await file.read()

        size_mb = len(contents) / (1024 * 1024)

        await file.seek(0)

        if size_mb > max_size_mb:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"Maximum file size is {max_size_mb} MB.",
            )

    # =====================================================
    # Random Filename
    # =====================================================

    @staticmethod
    def random_filename(
        extension: str,
    ) -> str:
        """
        Generate a secure random filename.
        """

        return (
            f"{secrets.token_hex(16)}{extension}"
        )


# ==========================================================
# Singleton
# ==========================================================

security_manager = SecurityManager()