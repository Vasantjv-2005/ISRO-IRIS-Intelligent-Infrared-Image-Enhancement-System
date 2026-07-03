"""
Analysis Repository

Handles all database operations related to AI scene analysis.
"""

from __future__ import annotations

from typing import List

from motor.motor_asyncio import AsyncIOMotorCollection

from app.database.mongodb import get_database
from app.models.analysis_model import (
    AnalysisModel,
    AnalysisStatus,
    utc_now,
)
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


class AnalysisRepository:
    """
    Repository responsible for Analyses collection.
    """

    COLLECTION = "analyses"

    @property
    def collection(self) -> AsyncIOMotorCollection:
        """
        Return MongoDB analyses collection.
        """

        db = get_database()

        return db[self.COLLECTION]

    # =====================================================
    # Create
    # =====================================================

    async def create(
        self,
        analysis: AnalysisModel,
    ) -> AnalysisModel:
        """
        Insert a new analysis document.
        """

        document = analysis.model_dump()

        await self.collection.insert_one(document)

        logger.info(
            "Analysis created: %s",
            analysis.analysis_id,
        )

        return analysis

    # =====================================================
    # Find by Analysis ID
    # =====================================================

    async def get_by_analysis_id(
        self,
        analysis_id: str,
    ) -> AnalysisModel | None:
        """
        Find analysis by analysis_id.
        """

        document = await self.collection.find_one(
            {
                "analysis_id": analysis_id
            }
        )

        if document is None:
            return None

        document.pop("_id", None)

        return AnalysisModel(**document)

    # =====================================================
    # Find by Upload ID
    # =====================================================

    async def get_by_upload_id(
        self,
        upload_id: str,
    ) -> AnalysisModel | None:
        """
        Find analysis by upload_id.
        """

        document = await self.collection.find_one(
            {
                "upload_id": upload_id
            }
        )

        if document is None:
            return None

        document.pop("_id", None)

        return AnalysisModel(**document)

    # =====================================================
    # Find by Image Name
    # =====================================================

    async def get_by_image_name(
        self,
        image_name: str,
    ) -> AnalysisModel | None:
        """
        Find analysis by image_name.
        """

        document = await self.collection.find_one(
            {
                "image_name": image_name
            }
        )

        if document is None:
            return None

        document.pop("_id", None)

        return AnalysisModel(**document)

    # =====================================================
    # List Analyses
    # =====================================================

    async def list_analyses(
        self,
        limit: int = 100,
    ) -> List[AnalysisModel]:
        """
        Return latest analyses.
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

        analyses: List[AnalysisModel] = []

        async for document in cursor:

            document.pop("_id", None)

            analyses.append(
                AnalysisModel(**document)
            )

        return analyses

    # =====================================================
    # Update Status
    # =====================================================

    async def update_status(
        self,
        analysis_id: str,
        status: AnalysisStatus,
    ) -> bool:
        """
        Update processing status.
        """

        updates = {
            "status": status,
            "updated_at": utc_now(),
        }

        if status == AnalysisStatus.COMPLETED:
            updates["analyzed_at"] = utc_now()

        result = await self.collection.update_one(
            {
                "analysis_id": analysis_id
            },
            {
                "$set": updates
            },
        )

        return result.modified_count > 0

    # =====================================================
    # Update Results
    # =====================================================

    async def update_results(
        self,
        analysis_id: str,
        *,
        scene_summary: str,
        detailed_analysis: str,
        detected_objects: list,
        object_count: int,
        confidence_score: float,
    ) -> bool:
        """
        Update AI scene analysis results.
        """

        result = await self.collection.update_one(
            {
                "analysis_id": analysis_id
            },
            {
                "$set": {
                    "status": AnalysisStatus.COMPLETED,
                    "scene_summary": scene_summary,
                    "detailed_analysis": detailed_analysis,
                    "detected_objects": detected_objects,
                    "object_count": object_count,
                    "confidence_score": confidence_score,
                    "analyzed_at": utc_now(),
                    "updated_at": utc_now(),
                }
            },
        )

        return result.modified_count > 0

    # =====================================================
    # Delete
    # =====================================================

    async def delete(
        self,
        analysis_id: str,
    ) -> bool:
        """
        Delete analysis by analysis_id.
        """

        result = await self.collection.delete_one(
            {
                "analysis_id": analysis_id
            }
        )

        return result.deleted_count > 0

    # =====================================================
    # Exists
    # =====================================================

    async def exists(
        self,
        analysis_id: str,
    ) -> bool:
        """
        Check if analysis exists.
        """

        count = await self.collection.count_documents(
            {
                "analysis_id": analysis_id
            },
            limit=1,
        )

        return count > 0

    # =====================================================
    # Count
    # =====================================================

    async def count(self) -> int:
        """
        Return total analysis documents.
        """

        return await self.collection.count_documents({})


# ==========================================================
# Singleton
# ==========================================================

analysis_repository = AnalysisRepository()
