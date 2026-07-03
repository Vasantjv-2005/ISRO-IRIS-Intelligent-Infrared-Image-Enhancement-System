"""
Dashboard Repository

Handles database operations for dashboard statistics and system health metrics.
"""

from __future__ import annotations

from typing import Any

from motor.motor_asyncio import AsyncIOMotorCollection

from app.database.mongodb import get_database
from app.models.dashboard_model import (
    DashboardModel,
    utc_now,
)
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


class DashboardRepository:
    """
    Repository responsible for Dashboard statistics collection.
    """

    COLLECTION = "dashboard_stats"
    STATS_ID = "stats"

    @property
    def collection(self) -> AsyncIOMotorCollection:
        """
        Return MongoDB dashboard statistics collection.
        """

        db = get_database()

        return db[self.COLLECTION]

    # =====================================================
    # Get Statistics
    # =====================================================

    async def get_statistics(self) -> DashboardModel:
        """
        Retrieve dashboard statistics or initialize defaults if not found.
        """

        document = await self.collection.find_one(
            {
                "dashboard_id": self.STATS_ID
            }
        )

        if document is None:

            default_stats = DashboardModel(dashboard_id=self.STATS_ID)

            await self.collection.insert_one(
                default_stats.model_dump()
            )

            return default_stats

        document.pop("_id", None)

        return DashboardModel(**document)

    # =====================================================
    # Save Statistics
    # =====================================================

    async def save_statistics(
        self,
        stats: DashboardModel,
    ) -> DashboardModel:
        """
        Upsert complete dashboard statistics document.
        """

        document = stats.model_dump()

        await self.collection.update_one(
            {
                "dashboard_id": self.STATS_ID
            },
            {
                "$set": document
            },
            upsert=True,
        )

        return stats

    # =====================================================
    # Increment Counters
    # =====================================================

    async def increment_counters(
        self,
        *,
        uploads: int = 0,
        processed_images: int = 0,
        reports: int = 0,
        objects_detected: int = 0,
        completed_analysis: int = 0,
        failed_jobs: int = 0,
    ) -> bool:
        """
        Atomically increment dashboard operational counters.
        """

        inc_fields: dict[str, int] = {}

        if uploads != 0:
            inc_fields["total_uploads"] = uploads

        if processed_images != 0:
            inc_fields["total_processed_images"] = processed_images

        if reports != 0:
            inc_fields["total_reports_generated"] = reports

        if objects_detected != 0:
            inc_fields["total_objects_detected"] = objects_detected

        if completed_analysis != 0:
            inc_fields["total_completed_analysis"] = completed_analysis

        if failed_jobs != 0:
            inc_fields["total_failed_jobs"] = failed_jobs

        if not inc_fields:
            return False

        result = await self.collection.update_one(
            {
                "dashboard_id": self.STATS_ID
            },
            {
                "$inc": inc_fields,
                "$set": {
                    "updated_at": utc_now()
                },
            },
            upsert=True,
        )

        return result.modified_count > 0 or result.upserted_id is not None

    # =====================================================
    # Update Metrics
    # =====================================================

    async def update_metrics(
        self,
        *,
        success_rate: float | None = None,
        avg_processing_time: float | None = None,
        storage_used_mb: float | None = None,
        active_sessions: int | None = None,
        system_status: str | None = None,
    ) -> bool:
        """
        Update performance and system health metrics.
        """

        updates: dict[str, Any] = {
            "updated_at": utc_now()
        }

        if success_rate is not None:
            updates["processing_success_rate"] = success_rate

        if avg_processing_time is not None:
            updates["average_processing_time_seconds"] = avg_processing_time

        if storage_used_mb is not None:
            updates["storage_used_mb"] = storage_used_mb

        if active_sessions is not None:
            updates["active_sessions"] = active_sessions

        if system_status is not None:
            updates["system_status"] = system_status

        result = await self.collection.update_one(
            {
                "dashboard_id": self.STATS_ID
            },
            {
                "$set": updates
            },
            upsert=True,
        )

        return result.modified_count > 0 or result.upserted_id is not None


# ==========================================================
# Singleton
# ==========================================================

dashboard_repository = DashboardRepository()
