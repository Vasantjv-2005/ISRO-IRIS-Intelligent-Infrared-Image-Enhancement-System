"""
Dashboard Service

Provides dashboard statistics for the IRIS Backend.
"""

from __future__ import annotations

from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorDatabase


class DashboardService:
    """
    Dashboard service.
    """

    def __init__(self) -> None:
        pass

    async def get_dashboard(
        self,
        db: AsyncIOMotorDatabase,
    ) -> dict:
        """
        Return dashboard statistics.
        """

        uploads = db.uploads
        reports = db.reports

        total_uploads = await uploads.count_documents({})

        total_reports = await reports.count_documents({})

        latest_upload = await uploads.find_one(
            sort=[("created_at", -1)]
        )

        return {
            "success": True,
            "generated_at": datetime.utcnow().isoformat(),
            "statistics": {
                "total_uploads": total_uploads,
                "total_reports": total_reports,
            },
            "latest_upload": latest_upload,
        }


dashboard_service = DashboardService()