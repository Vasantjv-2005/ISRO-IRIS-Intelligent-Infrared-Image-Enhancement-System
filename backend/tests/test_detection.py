"""
Tests for AI Detection Service.
"""

from __future__ import annotations

import unittest

from app.middleware.error_handler import ImageProcessingException
from app.services.ai.detection_service import detection_service


class TestDetectionService(unittest.TestCase):
    """
    Tests for DetectionService.
    """

    def test_detect_runs_on_valid_weights(self) -> None:
        """
        Since weights/detection/yolov8.pt is now a valid YOLO model,
        running detection on a non-existent image should bypass model loading
        and fail with 'Image not found' error.
        """
        with self.assertRaises(ImageProcessingException) as ctx:
            detection_service.detect(
                image_path="completely_non_existent_image.jpg",
                output_directory="dummy_out",
            )
        self.assertIn("Image not found", str(ctx.exception))
