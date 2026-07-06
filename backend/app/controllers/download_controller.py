"""
Download Controller

Handles file download requests by delegating to Download Service.
"""

from __future__ import annotations

from typing import Any

from app.services.download.download_service import download_service


class DownloadController:
    """
    Controller responsible for file download operations.
    """

    def get_file(
        self,
        file_path: str,
    ) -> dict[str, Any]:
        """
        Retrieve file metadata and path for download.
        """
        return download_service.get_file(file_path)


download_controller = DownloadController()
