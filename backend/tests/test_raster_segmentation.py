"""
Tests for Satellite Raster Segmentation Integration Module.
Verifies multi-band raster stream parsing, infrared spectrum isolation,
thresholding segmentation of water bodies vs forest canopy, and runtime optimization.
"""

from __future__ import annotations

import io
import tempfile
import unittest
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

from app.middleware.error_handler import ImageProcessingException
from app.services.image_processing.raster_segmentation import (
    RasterSegmentationService,
    raster_segmentation_service,
)


class TestRasterSegmentationService(unittest.TestCase):
    """
    Unit tests for RasterSegmentationService.
    """

    def setUp(self) -> None:
        self.service = RasterSegmentationService()
        # Create synthetic 4-band raster: (Height=120, Width=120, Bands=4)
        # Band 3 (NIR/IR band):
        # Top half (rows 0..59) = low infrared reflectance (e.g. water bodies ~ 30)
        # Bottom half (rows 60..119) = high infrared reflectance (e.g. forest canopy ~ 200)
        self.height, self.width = 120, 120
        self.synthetic_raster = np.zeros((self.height, self.width, 4), dtype=np.uint8)
        self.synthetic_raster[:60, :, 3] = 30   # Water bodies (low IR reflectance)
        self.synthetic_raster[60:, :, 3] = 210  # Forest canopy (high IR reflectance)

    def test_parse_raster_stream_from_numpy(self) -> None:
        """Test parsing raster directly from a numpy array."""
        arr = self.service.parse_raster_stream(self.synthetic_raster)
        self.assertEqual(arr.shape, (120, 120, 4))

    def test_parse_raster_stream_from_bytes_npz(self) -> None:
        """Test parsing raster stream from memory bytes stream (.npz archive)."""
        buffer = io.BytesIO()
        np.savez_compressed(buffer, raster=self.synthetic_raster)
        buffer.seek(0)
        arr = self.service.parse_raster_stream(buffer.read())
        self.assertEqual(arr.shape, (120, 120, 4))

    def test_parse_raster_stream_from_image_path(self) -> None:
        """Test parsing raster stream from an image file path."""
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            tmp_path = tmp.name
        try:
            # Save 3-band RGB image
            img_arr = np.full((80, 80, 3), 128, dtype=np.uint8)
            Image.fromarray(img_arr).save(tmp_path)
            arr = self.service.parse_raster_stream(tmp_path)
            self.assertEqual(arr.shape, (80, 80, 3))
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def test_isolate_infrared_band(self) -> None:
        """Test isolating infrared spectrum data band."""
        ir_band = self.service.isolate_infrared_band(self.synthetic_raster, ir_band_idx=-1)
        self.assertEqual(ir_band.shape, (120, 120))
        self.assertAlmostEqual(float(np.mean(ir_band[:60, :])), 30.0, delta=1.0)
        self.assertAlmostEqual(float(np.mean(ir_band[60:, :])), 210.0, delta=1.0)

    def test_isolate_infrared_band_invalid_index(self) -> None:
        """Test invalid band index raises ValueError / ImageProcessingException."""
        with self.assertRaises(ImageProcessingException):
            self.service.isolate_infrared_band(self.synthetic_raster, ir_band_idx=99)

    def test_compute_segmentation_threshold(self) -> None:
        """Test computing segmentation threshold using Otsu, Percentile, and Isodata methods."""
        ir_band = self.service.isolate_infrared_band(self.synthetic_raster, ir_band_idx=-1)

        t_otsu = self.service.compute_segmentation_threshold(ir_band, method="otsu")
        self.assertTrue(40.0 < t_otsu < 190.0, f"Otsu threshold {t_otsu} should separate 30 and 210")

        t_percentile = self.service.compute_segmentation_threshold(ir_band, method="percentile")
        self.assertTrue(t_percentile > 0.0)

        t_isodata = self.service.compute_segmentation_threshold(ir_band, method="isodata")
        self.assertTrue(40.0 < t_isodata < 190.0)

    def test_segment_water_and_canopy(self) -> None:
        """Test thresholding segmentation into water bodies vs forest canopy masks."""
        ir_band = self.service.isolate_infrared_band(self.synthetic_raster, ir_band_idx=-1)
        t = 120.0
        water_mask, forest_mask = self.service.segment_water_and_canopy(ir_band, threshold=t)

        self.assertEqual(water_mask.shape, (120, 120))
        self.assertEqual(forest_mask.shape, (120, 120))
        # Top half (< 120) should be water
        self.assertTrue(np.all(water_mask[:58, :] == 255))
        # Bottom half (>= 120) should be forest canopy
        self.assertTrue(np.all(forest_mask[62:, :] == 255))

    def test_create_colorized_segmentation_map(self) -> None:
        """Test generating high quality aesthetic colorized segmentation map."""
        ir_band = self.service.isolate_infrared_band(self.synthetic_raster, ir_band_idx=-1)
        water_mask, forest_mask = self.service.segment_water_and_canopy(ir_band, threshold=120.0)
        color_map = self.service.create_colorized_segmentation_map(ir_band, water_mask, forest_mask)

        self.assertEqual(color_map.shape, (120, 120, 3))
        self.assertEqual(color_map.dtype, np.uint8)

    def test_process_raster_end_to_end_and_runtime_speed(self) -> None:
        """Test end-to-end process_raster execution speed and structured response."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_path = Path(tmp_dir) / "seg_out.jpg"

            result = raster_segmentation_service.process_raster(
                file_stream=self.synthetic_raster,
                ir_band_idx=-1,
                method="otsu",
                enhance_ir=True,
                output_path=out_path,
            )

            self.assertTrue(result["success"])
            self.assertEqual(result["shape"], (120, 120, 4))
            self.assertIn("threshold", result)
            self.assertIn("water_mask", result)
            self.assertIn("forest_mask", result)
            self.assertIn("runtime_ms", result)
            # Check optimization: execution should be fast (< 500ms for 120x120 raster)
            self.assertLess(result["runtime_ms"], 500.0)

            # Check coverage percentages
            self.assertGreater(result["water_coverage_pct"], 40.0)
            self.assertGreater(result["forest_coverage_pct"], 40.0)

            # Check saved output map
            self.assertTrue(out_path.exists())


if __name__ == "__main__":
    unittest.main()
