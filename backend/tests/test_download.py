"""
Tests for Download Service and Controller.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from app.controllers.download_controller import download_controller


class TestDownloadService(unittest.TestCase):
    """
    Tests for DownloadService operations.
    """

    def test_get_file_success(self) -> None:
        """
        Verify get_file returns correct metadata for an existing file.
        """
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as tmp_file:
            tmp_file.write(b"Hello IRIS")
            tmp_path = tmp_file.name

        try:
            file_info = download_controller.get_file(tmp_path)
            self.assertEqual(file_info["path"], str(Path(tmp_path).resolve()))
            self.assertEqual(file_info["filename"], Path(tmp_path).name)
            self.assertEqual(file_info["mime_type"], "text/plain")
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def test_get_file_not_found(self) -> None:
        """
        Verify get_file raises FileNotFoundError for non-existent file.
        """
        with self.assertRaises(FileNotFoundError):
            download_controller.get_file("non_existent_file_12345.txt")
