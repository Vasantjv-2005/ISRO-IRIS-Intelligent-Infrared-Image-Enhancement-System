"""
Tests for Pipeline Service.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

from app.schemas.pipeline_schema import PipelineRequestSchema
from app.services.pipeline.pipeline_service import pipeline_service


class TestPipelineService(unittest.IsolatedAsyncioTestCase):
    """
    Tests for PipelineService operations.
    """

    @patch("app.services.pipeline.pipeline_service.upload_repository")
    @patch("app.services.pipeline.pipeline_service.enhancement_service")
    @patch("app.services.pipeline.pipeline_service.colorization_service")
    @patch("app.services.pipeline.pipeline_service.detection_service")
    @patch("app.services.pipeline.pipeline_service.analysis_service")
    @patch("app.services.pipeline.pipeline_service.report_generation_service")
    @patch("app.services.pipeline.pipeline_service.comparison_service")
    async def test_run_pipeline_success(
        self,
        mock_comp,
        mock_report,
        mock_analysis,
        mock_detection,
        mock_color,
        mock_enhance,
        mock_upload_repo,
    ) -> None:
        """
        Verify end-to-end pipeline execution.
        """
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_in:
            in_path = tmp_in.name

        try:
            mock_upload_repo.update_status = AsyncMock()
            mock_upload_repo.exists = AsyncMock(return_value=True)
            mock_upload_repo.save_enhancement_path = AsyncMock()
            mock_upload_repo.save_colorization_path = AsyncMock()
            mock_upload_repo.save_detection_results = AsyncMock()
            mock_enhance.enhance.return_value = "enhanced.jpg"
            mock_color.colorize.return_value = "colorized.jpg"
            mock_detection.detect.return_value = {
                "detections": [],
                "total_objects": 0,
            }
            mock_analysis.analyze_async = AsyncMock(return_value={
                "analysis": "No thermal objects detected.",
            })
            mock_report.generate_report_async = AsyncMock(return_value="report.pdf")
            mock_comp.compare = AsyncMock(return_value=MagicMock(similarity_score=95.0))

            request = PipelineRequestSchema(
                image_path=in_path,
                confidence=0.25,
            )

            res = await pipeline_service.run_pipeline(request, upload_id="upload_123")
            self.assertTrue(res.success)
            self.assertEqual(res.upload_id, "upload_123")
            self.assertIn("enhanced_", res.enhanced_image)
        finally:
            Path(in_path).unlink(missing_ok=True)
