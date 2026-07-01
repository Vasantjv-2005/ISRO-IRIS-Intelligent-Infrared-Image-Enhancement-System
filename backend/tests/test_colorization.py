"""
Tests for AI Colorization Service.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import cv2
import numpy as np

from app.services.ai.colorization_service import colorization_service


class TestColorizationService(unittest.TestCase):
    """
    Tests for ColorizationService.
    """

    def test_colorize_file_success(self) -> None:
        """
        Test colorize with file paths using the service.
        """
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_in:
            in_path = tmp_in.name
            dummy_img = np.zeros((100, 100), dtype=np.uint8)
            cv2.imwrite(in_path, dummy_img)

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_out:
            out_path = tmp_out.name

        try:
            res_path = colorization_service.colorize(in_path, tmp_out.name)
            self.assertEqual(res_path, out_path)
            colorized = cv2.imread(res_path)
            self.assertIsNotNone(colorized)
            self.assertEqual(colorized.shape[2], 3)
        finally:
            Path(in_path).unlink(missing_ok=True)
            Path(out_path).unlink(missing_ok=True)

    def test_colorize_array_success(self) -> None:
        """
        Test colorize_array using the service.
        """
        dummy_img = np.zeros((100, 100), dtype=np.uint8)
        colorized = colorization_service.colorize_array(dummy_img)
        self.assertIsNotNone(colorized)
        self.assertEqual(colorized.shape[2], 3)
