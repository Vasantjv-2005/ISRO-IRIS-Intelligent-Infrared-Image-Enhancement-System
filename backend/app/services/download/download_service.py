"""
Download Service

Provides file download functionality for
generated images and reports.
"""

from __future__ import annotations

import mimetypes
from pathlib import Path


class DownloadService:
    """
    Service responsible for validating and preparing
    files for download.
    """

    def __init__(self) -> None:
        pass

    # =====================================================
    # Get File
    # =====================================================

    def get_file(
        self,
        file_path: str,
    ) -> dict:
        """
        Validate and return file metadata.
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        if not path.is_file():
            raise IsADirectoryError(
                f"Expected a file but received a directory: {file_path}"
            )

        mime_type, _ = mimetypes.guess_type(
            str(path)
        )

        return {
            "path": str(path.resolve()),
            "filename": path.name,
            "size": path.stat().st_size,
            "mime_type": mime_type
            or "application/octet-stream",
        }

    # =====================================================
    # File Exists
    # =====================================================

    def exists(
        self,
        file_path: str,
    ) -> bool:
        """
        Check whether a file exists.
        """

        return Path(file_path).exists()

    # =====================================================
    # Delete File
    # =====================================================

    def delete_file(
        self,
        file_path: str,
    ) -> bool:
        """
        Delete a file.
        """

        path = Path(file_path)

        if not path.exists():
            return False

        path.unlink()

        return True

    # =====================================================
    # Get File Size
    # =====================================================

    def get_size(
        self,
        file_path: str,
    ) -> int:
        """
        Return file size in bytes.
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        return path.stat().st_size

    # =====================================================
    # Get Extension
    # =====================================================

    def get_extension(
        self,
        file_path: str,
    ) -> str:
        """
        Return file extension.
        """

        return Path(file_path).suffix.lower()


# ==========================================================
# Singleton
# ==========================================================

download_service = DownloadService()