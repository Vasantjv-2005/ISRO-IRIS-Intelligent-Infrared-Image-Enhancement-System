"""
Tests for Preprocessing Service.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from app.middleware.error_handler import ImageProcessingException
from app.services.image_processing.preprocessing_service import (
    preprocessing_service,
)


class TestPreprocessingService(unittest.TestCase):
    """
    Tests for PreprocessingService operations.
    """

    @patch("app.services.image_processing.resize.resize_service.resize")
    @patch("app.services.image_processing.normalization.normalization_service.normalize")
    @patch("app.services.image_processing.noise_reduction.noise_reduction_service.reduce_noise")
    @patch("app.services.image_processing.contrast_enhancement.contrast_enhancement_service.enhance")
    @patch("app.services.image_processing.crop.crop_service.crop")
    def test_process_success(
        self,
        mock_crop: MagicMock,
        mock_enhance: MagicMock,
        mock_denoise: MagicMock,
        mock_normalize: MagicMock,
        mock_resize: MagicMock,
    ) -> None:
        """
        Verify that preprocessing service runs the entire pipeline successfully.
        """
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_in:
            in_path = tmp_in.name

        with tempfile.TemporaryDirectory() as tmp_out_dir:
            out_dir = tmp_out_dir

            result = preprocessing_service.process(
                input_path=in_path,
                output_directory=out_dir,
                apply_crop=True,
            )

            self.assertTrue(result["success"])
            self.assertEqual(result["input_image"], in_path)
            self.assertEqual(result["output_directory"], out_dir)
            self.assertIsNotNone(result["steps"]["cropped"])

            # Verify services called
            mock_resize.assert_called_once()
            mock_normalize.assert_called_once()
            mock_denoise.assert_called_once()
            mock_enhance.assert_called_once()
            mock_crop.assert_called_once()

        # Clean up
        Path(in_path).unlink(missing_ok=True)

    def test_process_missing_image_raises_exception(self) -> None:
        """
        Verify that missing input image raises ImageProcessingException.
        """
        with self.assertRaises(ImageProcessingException):
            preprocessing_service.process(
                input_path="missing_file_path.jpg",
                output_directory="dummy_dir",
            )
