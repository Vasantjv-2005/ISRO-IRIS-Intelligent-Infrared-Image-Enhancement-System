"""
Tests for Dashboard and Comparison Services.
"""

from __future__ import annotations

import unittest
from unittest.mock import AsyncMock, MagicMock

from app.services.dashboard.dashboard_service import dashboard_service


class TestDashboardService(unittest.IsolatedAsyncioTestCase):
    """
    Tests for DashboardService operations.
    """

    async def test_get_dashboard_success(self) -> None:
        """
        Verify get_dashboard aggregates data and returns correct stats.
        """
        mock_db = MagicMock()
        
        # Mock database collection calls
        mock_uploads = AsyncMock()
        mock_uploads.count_documents.side_effect = [10, 5, 4, 3, 1]  # uploads, processed, reports, analysis, failed
        
        # Mock aggregations
        mock_cursor = MagicMock()
        mock_cursor.to_list = AsyncMock(return_value=[{"total": 12, "total_size": 20971520}])
        mock_uploads.aggregate = MagicMock(return_value=mock_cursor)

        mock_sessions = AsyncMock()
        mock_sessions.count_documents.return_value = 2  # active sessions
        
        mock_cursor_time = MagicMock()
        mock_cursor_time.to_list = AsyncMock(return_value=[{"avg_time": 4.5}])
        mock_sessions.aggregate = MagicMock(return_value=mock_cursor_time)

        # Mock recent uploads finder
        mock_recent_cursor = MagicMock()
        mock_recent_cursor.sort.return_value.limit.return_value = mock_recent_cursor
        # Define mock async iterator
        async def mock_async_iter(*args, **kwargs):
            yield {
                "upload_id": "upload_1",
                "filename": "test1.jpg",
                "status": "completed",
                "uploaded_at": None,
            }
        mock_recent_cursor.__aiter__ = mock_async_iter
        mock_uploads.find = MagicMock(return_value=mock_recent_cursor)

        mock_db.__getitem__.side_effect = lambda name: mock_uploads if name == "uploads" else mock_sessions

        result = await dashboard_service.get_dashboard(mock_db)

        self.assertEqual(result["statistics"]["total_uploads"], 10)
        self.assertEqual(result["statistics"]["total_processed_images"], 5)
        self.assertEqual(result["statistics"]["total_reports_generated"], 4)
        self.assertEqual(result["statistics"]["total_objects_detected"], 12)
        self.assertEqual(result["statistics"]["active_sessions"], 2)
        self.assertEqual(result["statistics"]["average_processing_time_seconds"], 4.5)
        self.assertEqual(result["statistics"]["storage_used_mb"], 20.0)
        self.assertEqual(len(result["recent_activities"]), 1)
