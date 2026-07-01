"""
Tests for AI Report Generation Service.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from app.middleware.error_handler import ReportGenerationException
from app.services.ai.report_generation_service import (
    report_generation_service,
)


class TestReportGenerationService(unittest.TestCase):
    """
    Tests for ReportGenerationService operations.
    """

    def test_generate_report_success(self) -> None:
        """
        Verify that PDF reports are successfully built and saved.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            pdf_path = Path(tmp_dir) / "test_report.pdf"

            res_path = report_generation_service.generate_report(
                report_path=str(pdf_path),
                image_name="thermal_ir.jpg",
                detected_objects=[
                    {"class_id": 0, "class_name": "vehicle", "confidence": 0.88, "bbox": [100, 200, 150, 250]}
                ],
                analysis="Mocked analysis text for testing reportlab generation.",
            )

            self.assertEqual(res_path, str(pdf_path))
            self.assertTrue(pdf_path.exists())
            self.assertGreater(pdf_path.stat().st_size, 0)

    def test_generate_report_failure_raises_exception(self) -> None:
        """
        Verify that passing invalid directory/path raises ReportGenerationException.
        """
        # Using an invalid path like an empty string or illegal path should raise an exception
        with self.assertRaises(ReportGenerationException):
            report_generation_service.generate_report(
                report_path="",  # Invalid output path
                image_name="test.jpg",
                detected_objects=[],
                analysis="Dummy text",
            )
