"""
Tests for Comparison Service and Controller.
"""

from __future__ import annotations

import numpy as np
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from app.models.comparison_model import ComparisonModel, ComparisonStatus
from app.controllers.comparison_controller import comparison_controller


class TestComparisonService(unittest.IsolatedAsyncioTestCase):
    """
    Tests for ComparisonService operations.
    """

    @patch("app.services.dashboard.comparison_service.upload_repository")
    @patch("app.services.dashboard.comparison_service.comparison_repository")
    @patch("app.services.dashboard.comparison_service.cv2.imread")
    @patch("app.services.dashboard.comparison_service.cv2.imwrite")
    async def test_compare_success(
        self,
        mock_imwrite,
        mock_imread,
        mock_comp_repo,
        mock_upload_repo,
    ) -> None:
        """
        Verify comparison service runs image comparison successfully.
        """
        mock_upload = MagicMock()
        mock_upload.file_path = "uploads/test.jpg"
        mock_upload.enhancement_completed = True
        mock_upload.colorization_completed = True
        mock_upload.detection_completed = True
        mock_upload.analysis_completed = True
        mock_upload.objects_detected = ["object1"]
        mock_upload.scene_summary = "Test summary"
        mock_upload_repo.get_by_upload_id = AsyncMock(return_value=mock_upload)

        mock_imread.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
        mock_imwrite.return_value = True

        mock_comp_model = ComparisonModel(
            upload_id="upload_123",
            status=ComparisonStatus.COMPLETED,
            original_image_path="uploads/test.jpg",
            processed_image_path="uploads/test.jpg",
            comparison_image_path="outputs/comparisons/test_comparison.jpg",
            similarity_score=100.0,
        )
        mock_comp_repo.save = AsyncMock(return_value=mock_comp_model)
        mock_comp_repo.upsert_by_upload_id = AsyncMock(return_value=mock_comp_model)

        res = await comparison_controller.compare_images(db=None, upload_id="upload_123")
        self.assertEqual(res.upload_id, "upload_123")
        self.assertEqual(res.status, ComparisonStatus.COMPLETED)
