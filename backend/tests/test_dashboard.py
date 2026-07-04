"""
Tests for Dashboard and Comparison Services.
"""

from __future__ import annotations

import unittest
from unittest.mock import AsyncMock, patch

from app.services.dashboard.dashboard_service import dashboard_service


class TestDashboardService(unittest.IsolatedAsyncioTestCase):
    """
    Tests for DashboardService operations.
    """

    @patch("app.services.dashboard.dashboard_service.session_repository")
    @patch("app.services.dashboard.dashboard_service.upload_repository")
    async def test_get_dashboard_success(
        self,
        mock_upload_repo: AsyncMock,
        mock_session_repo: AsyncMock,
    ) -> None:
        """
        Verify get_dashboard aggregates data from repositories and returns correct stats.
        """
        mock_upload_repo.get_upload_statistics = AsyncMock(
            return_value={
                "total_uploads": 10,
                "total_processed_images": 5,
                "total_reports_generated": 4,
                "total_completed_analysis": 3,
                "total_failed_jobs": 1,
                "total_objects_detected": 12,
                "total_size_bytes": 20971520,
            }
        )
        mock_upload_repo.get_recent_uploads = AsyncMock(
            return_value=[
                {
                    "upload_id": "upload_1",
                    "filename": "test1.jpg",
                    "status": "completed",
                    "uploaded_at": "2026-07-04T00:00:00Z",
                }
            ]
        )
        mock_session_repo.get_session_statistics = AsyncMock(
            return_value={
                "active_sessions": 2,
                "average_processing_time_seconds": 4.5,
            }
        )

        result = await dashboard_service.get_dashboard()

        self.assertEqual(result["statistics"]["total_uploads"], 10)
        self.assertEqual(result["statistics"]["total_processed_images"], 5)
        self.assertEqual(result["statistics"]["total_reports_generated"], 4)
        self.assertEqual(result["statistics"]["total_objects_detected"], 12)
        self.assertEqual(result["statistics"]["active_sessions"], 2)
        self.assertEqual(result["statistics"]["average_processing_time_seconds"], 4.5)
        self.assertEqual(result["statistics"]["storage_used_mb"], 20.0)
        self.assertEqual(len(result["recent_activities"]), 1)

