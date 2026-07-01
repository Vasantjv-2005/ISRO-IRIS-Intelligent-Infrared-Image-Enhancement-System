"""
Tests for AI Enhancement Service.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import cv2
import numpy as np

from app.services.ai.enhancement_service import enhancement_service


class TestEnhancementService(unittest.TestCase):
    """
    Tests for EnhancementService.
    """

    def test_enhance_file_success(self) -> None:
        """
        Test enhance with file paths using the service.
        """
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_in:
            in_path = tmp_in.name
            dummy_img = np.zeros((100, 100, 3), dtype=np.uint8)
            cv2.imwrite(in_path, dummy_img)

        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_out:
            out_path = tmp_out.name

        try:
            res_path = enhancement_service.enhance(in_path, out_path)
            self.assertEqual(res_path, out_path)
            enhanced = cv2.imread(res_path)
            self.assertIsNotNone(enhanced)
        finally:
            Path(in_path).unlink(missing_ok=True)
            Path(out_path).unlink(missing_ok=True)

    def test_enhance_array_success(self) -> None:
        """
        Test enhance_array using the service.
        """
        dummy_img = np.zeros((100, 100, 3), dtype=np.uint8)
        enhanced = enhancement_service.enhance_array(dummy_img)
        self.assertIsNotNone(enhanced)
