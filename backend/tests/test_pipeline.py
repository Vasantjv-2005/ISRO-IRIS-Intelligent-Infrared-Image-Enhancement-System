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
    @patch("app.services.pipeline.pipeline_service.preprocessing_service")
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
        mock_preproc,
        mock_upload_repo,
    ) -> None:
        """
        Verify end-to-end sequential pipeline execution.
        """
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_in:
            in_path = tmp_in.name

        try:
            mock_upload_repo.update_status = AsyncMock()
            mock_upload_repo.exists = AsyncMock(return_value=True)
            mock_upload_repo.save_preprocessing_path = AsyncMock()
            mock_upload_repo.save_enhancement_path = AsyncMock()
            mock_upload_repo.save_colorization_path = AsyncMock()
            mock_upload_repo.save_detection_results = AsyncMock()
            mock_preproc.process.return_value = {"output_path": "preprocessed.jpg", "processed_image": "preprocessed.jpg"}
            mock_enhance.enhance.return_value = "enhanced.jpg"
            mock_color.colorize.return_value = "colorized.jpg"
            mock_detection.detect.return_value = {
                "detections": [],
                "total_objects": 0,
                "output_path": "detected.jpg",
            }
            mock_analysis.analyze_async = AsyncMock(return_value={
                "analysis": "No thermal objects detected.",
                "output_path": "analyzed.jpg",
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
            self.assertEqual(res.preprocessed_image, "preprocessed.jpg")
            self.assertEqual(res.enhanced_image, "enhanced.jpg")
            self.assertEqual(res.colorized_image, "colorized.jpg")
            self.assertEqual(res.detected_image, "detected.jpg")
            self.assertEqual(res.analyzed_image, "analyzed.jpg")
            mock_preproc.process.assert_called_once()
            mock_enhance.enhance.assert_called_once()
            mock_color.colorize.assert_called_once()
            mock_detection.detect.assert_called_once()
            mock_analysis.analyze_async.assert_called_once()
            mock_report.generate_report_async.assert_called_once()
        finally:
            Path(in_path).unlink(missing_ok=True)
