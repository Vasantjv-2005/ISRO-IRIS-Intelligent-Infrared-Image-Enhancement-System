"""
Comparison Repository

Handles all database operations related to image comparisons.
"""

from __future__ import annotations

from typing import List

from motor.motor_asyncio import AsyncIOMotorCollection

from app.database.mongodb import get_database
from app.models.comparison_model import (
    ComparisonModel,
    ComparisonStatus,
    utc_now,
)
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


class ComparisonRepository:
    """
    Repository responsible for Comparisons collection.
    """

    COLLECTION = "comparisons"

    @property
    def collection(self) -> AsyncIOMotorCollection:
        """
        Return MongoDB comparisons collection.
        """

        db = get_database()

        return db[self.COLLECTION]

    # =====================================================
    # Create
    # =====================================================

    async def create(
        self,
        comparison: ComparisonModel,
    ) -> ComparisonModel:
        """
        Insert a new comparison document.
        """

        document = comparison.model_dump()

        await self.collection.insert_one(document)

        logger.info(
            "Comparison created: %s",
            comparison.comparison_id,
        )

        return comparison

    # =====================================================
    # Find by Comparison ID
    # =====================================================

    async def get_by_comparison_id(
        self,
        comparison_id: str,
    ) -> ComparisonModel | None:
        """
        Find comparison by comparison_id.
        """

        document = await self.collection.find_one(
            {
                "comparison_id": comparison_id
            }
        )

        if document is None:
            return None

        document.pop("_id", None)

        return ComparisonModel(**document)

    # =====================================================
    # Find by Upload ID
    # =====================================================

    async def get_by_upload_id(
        self,
        upload_id: str,
    ) -> ComparisonModel | None:
        """
        Find comparison by upload_id.
        """

        document = await self.collection.find_one(
            {
                "upload_id": upload_id
            }
        )

        if document is None:
            return None

        document.pop("_id", None)

        return ComparisonModel(**document)

    # =====================================================
    # List Comparisons
    # =====================================================

    async def list_comparisons(
        self,
        limit: int = 100,
    ) -> List[ComparisonModel]:
        """
        Return latest comparisons.
        """

        cursor = (
            self.collection
            .find()
            .sort(
                "created_at",
                -1,
            )
            .limit(limit)
        )

        comparisons: List[ComparisonModel] = []

        async for document in cursor:

            document.pop("_id", None)

            comparisons.append(
                ComparisonModel(**document)
            )

        return comparisons

    # =====================================================
    # Update Status
    # =====================================================

    async def update_status(
        self,
        comparison_id: str,
        status: ComparisonStatus,
    ) -> bool:
        """
        Update processing status.
        """

        result = await self.collection.update_one(
            {
                "comparison_id": comparison_id
            },
            {
                "$set": {
                    "status": status,
                    "updated_at": utc_now(),
                }
            },
        )

        return result.modified_count > 0

    # =====================================================
    # Update Comparison Results
    # =====================================================

    async def update_comparison_results(
        self,
        comparison_id: str,
        *,
        comparison_image_path: str | None = None,
        similarity_score: float = 0.0,
        processing_time_seconds: float = 0.0,
        total_objects: int = 0,
        detected_objects: list | None = None,
        ai_summary: str | None = None,
    ) -> bool:
        """
        Update image comparison metrics and results.
        """

        updates = {
            "status": ComparisonStatus.COMPLETED,
            "similarity_score": similarity_score,
            "processing_time_seconds": processing_time_seconds,
            "total_objects": total_objects,
            "updated_at": utc_now(),
        }

        if comparison_image_path is not None:
            updates["comparison_image_path"] = comparison_image_path

        if detected_objects is not None:
            updates["detected_objects"] = detected_objects

        if ai_summary is not None:
            updates["ai_summary"] = ai_summary

        result = await self.collection.update_one(
            {
                "comparison_id": comparison_id
            },
            {
                "$set": updates
            },
        )

        return result.modified_count > 0

    # =====================================================
    # Delete
    # =====================================================

    async def delete(
        self,
        comparison_id: str,
    ) -> bool:
        """
        Delete comparison by comparison_id.
        """

        result = await self.collection.delete_one(
            {
                "comparison_id": comparison_id
            }
        )

        return result.deleted_count > 0

    # =====================================================
    # Exists
    # =====================================================

    async def exists(
        self,
        comparison_id: str,
    ) -> bool:
        """
        Check if comparison exists.
        """

        count = await self.collection.count_documents(
            {
                "comparison_id": comparison_id
            },
            limit=1,
        )

        return count > 0

    # =====================================================
    # Count
    # =====================================================

    async def count(self) -> int:
        """
        Return total comparison documents.
        """

        return await self.collection.count_documents({})

    # =====================================================
    # Upsert by Upload ID
    # =====================================================

    async def upsert_by_upload_id(
        self,
        comparison: ComparisonModel,
    ) -> ComparisonModel:
        """
        Update or insert comparison document by upload_id.
        """

        document = comparison.model_dump()
        await self.collection.update_one(
            {"upload_id": comparison.upload_id},
            {"$set": document},
            upsert=True,
        )
        logger.info("Comparison upserted for upload_id: %s", comparison.upload_id)
        return comparison


# ==========================================================
# Singleton
# ==========================================================

comparison_repository = ComparisonRepository()
