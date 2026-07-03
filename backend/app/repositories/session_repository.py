"""
Session Repository

Handles all database operations related to image processing sessions.
"""

from __future__ import annotations

from datetime import datetime
from typing import List

from motor.motor_asyncio import AsyncIOMotorCollection

from app.database.mongodb import get_database
from app.models.session_model import (
    SessionModel,
    SessionStatus,
    utc_now,
)
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


class SessionRepository:
    """
    Repository responsible for Sessions collection.
    """

    COLLECTION = "sessions"

    @property
    def collection(self) -> AsyncIOMotorCollection:
        """
        Return MongoDB sessions collection.
        """

        db = get_database()

        return db[self.COLLECTION]

    # =====================================================
    # Create
    # =====================================================

    async def create(
        self,
        session: SessionModel,
    ) -> SessionModel:
        """
        Insert a new session document.
        """

        document = session.model_dump()

        await self.collection.insert_one(document)

        logger.info(
            "Session created: %s",
            session.session_id,
        )

        return session

    # =====================================================
    # Find by Session ID
    # =====================================================

    async def get_by_session_id(
        self,
        session_id: str,
    ) -> SessionModel | None:
        """
        Find session by session_id.
        """

        document = await self.collection.find_one(
            {
                "session_id": session_id
            }
        )

        if document is None:
            return None

        document.pop("_id", None)

        return SessionModel(**document)

    # =====================================================
    # Find by Upload ID
    # =====================================================

    async def get_by_upload_id(
        self,
        upload_id: str,
    ) -> SessionModel | None:
        """
        Find session by upload_id.
        """

        document = await self.collection.find_one(
            {
                "upload_id": upload_id
            }
        )

        if document is None:
            return None

        document.pop("_id", None)

        return SessionModel(**document)

    # =====================================================
    # List Sessions
    # =====================================================

    async def list_sessions(
        self,
        limit: int = 100,
    ) -> List[SessionModel]:
        """
        Return latest sessions.
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

        sessions: List[SessionModel] = []

        async for document in cursor:

            document.pop("_id", None)

            sessions.append(
                SessionModel(**document)
            )

        return sessions

    # =====================================================
    # Update Status
    # =====================================================

    async def update_status(
        self,
        session_id: str,
        status: SessionStatus,
        error_message: str | None = None,
    ) -> bool:
        """
        Update processing status.
        """

        updates = {
            "status": status,
            "updated_at": utc_now(),
        }

        if status == SessionStatus.COMPLETED:
            updates["completed_at"] = utc_now()

        if error_message is not None:
            updates["error_message"] = error_message

        result = await self.collection.update_one(
            {
                "session_id": session_id
            },
            {
                "$set": updates
            },
        )

        return result.modified_count > 0

    # =====================================================
    # Update Progress
    # =====================================================

    async def update_progress(
        self,
        session_id: str,
        progress: int,
        current_stage: str,
    ) -> bool:
        """
        Update processing progress and stage.
        """

        result = await self.collection.update_one(
            {
                "session_id": session_id
            },
            {
                "$set": {
                    "progress": progress,
                    "current_stage": current_stage,
                    "updated_at": utc_now(),
                }
            },
        )

        return result.modified_count > 0

    # =====================================================
    # Complete Session
    # =====================================================

    async def complete_session(
        self,
        session_id: str,
        image_id: str | None = None,
        analysis_id: str | None = None,
        report_id: str | None = None,
        comparison_id: str | None = None,
        processing_time_seconds: float = 0.0,
    ) -> bool:
        """
        Mark session as completed and update related entity IDs.
        """

        updates = {
            "status": SessionStatus.COMPLETED,
            "progress": 100,
            "current_stage": "Completed",
            "processing_time_seconds": processing_time_seconds,
            "completed_at": utc_now(),
            "updated_at": utc_now(),
        }

        if image_id is not None:
            updates["image_id"] = image_id

        if analysis_id is not None:
            updates["analysis_id"] = analysis_id

        if report_id is not None:
            updates["report_id"] = report_id

        if comparison_id is not None:
            updates["comparison_id"] = comparison_id

        result = await self.collection.update_one(
            {
                "session_id": session_id
            },
            {
                "$set": updates
            },
        )

        return result.modified_count > 0

    # =====================================================
    # Fail Session
    # =====================================================

    async def fail_session(
        self,
        session_id: str,
        error_message: str,
    ) -> bool:
        """
        Mark session as failed with an error message.
        """

        result = await self.collection.update_one(
            {
                "session_id": session_id
            },
            {
                "$set": {
                    "status": SessionStatus.FAILED,
                    "error_message": error_message,
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
        session_id: str,
    ) -> bool:
        """
        Delete session by session_id.
        """

        result = await self.collection.delete_one(
            {
                "session_id": session_id
            }
        )

        return result.deleted_count > 0

    # =====================================================
    # Exists
    # =====================================================

    async def exists(
        self,
        session_id: str,
    ) -> bool:
        """
        Check if session exists.
        """

        count = await self.collection.count_documents(
            {
                "session_id": session_id
            },
            limit=1,
        )

        return count > 0

    # =====================================================
    # Count
    # =====================================================

    async def count(self) -> int:
        """
        Return total sessions.
        """

        return await self.collection.count_documents({})


# ==========================================================
# Singleton
# ==========================================================

session_repository = SessionRepository()
