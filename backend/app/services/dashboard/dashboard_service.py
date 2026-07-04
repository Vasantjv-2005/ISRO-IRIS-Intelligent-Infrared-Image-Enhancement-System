"""
Dashboard Service

Provides dashboard statistics for the IRIS Backend by querying repository layer.
"""

from __future__ import annotations

from typing import Any

from app.models.dashboard_model import utc_now
from app.repositories.session_repository import session_repository
from app.repositories.upload_repository import upload_repository
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


class DashboardService:
    """
    Dashboard service responsible for calculating metrics and stats.
    """

    async def get_dashboard(
        self,
        db: Any = None,
    ) -> dict:
        """
        Return dashboard statistics.

        Args:
            db: Optional database reference (ignored; kept for API compatibility).

        Returns:
            Dictionary containing dashboard statistics and recent activities.
        """
        logger.info("Aggregating dashboard statistics via repository layer.")
        upload_stats = await upload_repository.get_upload_statistics()
        session_stats = await session_repository.get_session_statistics()

        total_uploads = upload_stats["total_uploads"]
        total_processed = upload_stats["total_processed_images"]

        success_rate = 0.0
        if total_uploads > 0:
            success_rate = round((total_processed / total_uploads) * 100.0, 2)

        storage_mb = round(upload_stats["total_size_bytes"] / (1024 * 1024), 2)

        recent_activities = await upload_repository.get_recent_uploads(limit=5)

        logger.info("Successfully aggregated dashboard statistics.")
        return {
            "statistics": {
                "total_uploads": total_uploads,
                "total_processed_images": total_processed,
                "total_reports_generated": upload_stats["total_reports_generated"],
                "total_objects_detected": upload_stats["total_objects_detected"],
                "total_completed_analysis": upload_stats["total_completed_analysis"],
                "total_failed_jobs": upload_stats["total_failed_jobs"],
                "active_sessions": session_stats["active_sessions"],
                "processing_success_rate": success_rate,
                "average_processing_time_seconds": session_stats["average_processing_time_seconds"],
                "storage_used_mb": storage_mb,
            },
            "recent_activities": recent_activities,
            "system_health": {
                "backend_status": "Online",
                "database_status": "Connected",
                "ai_model_status": "Ready",
                "uptime": "24h 0m",
                "last_updated": utc_now(),
            },
        }


dashboard_service = DashboardService()