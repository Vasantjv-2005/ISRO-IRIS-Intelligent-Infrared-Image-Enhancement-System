"""
Session Service

Manages image processing sessions.
"""

from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.session_model import (
    SessionModel,
    SessionStatus,
)


class SessionService:
    """
    Service responsible for managing
    image processing sessions.
    """

    COLLECTION = "sessions"

    # =====================================================
    # Create Session
    # =====================================================

    async def create_session(
        self,
        db: AsyncIOMotorDatabase,
        upload_id: str,
    ) -> SessionModel:
        """
        Create a new processing session.
        """

        session = SessionModel(
            session_id=str(uuid4()),
            upload_id=upload_id,
        )

        await db[self.COLLECTION].insert_one(
            session.model_dump()
        )

        return session

    # =====================================================
    # Get Session
    # =====================================================

    async def get_session(
        self,
        db: AsyncIOMotorDatabase,
        session_id: str,
    ) -> SessionModel | None:
        """
        Get session by ID.
        """

        document = await db[self.COLLECTION].find_one(
            {
                "session_id": session_id
            }
        )

        if document is None:
            return None

        document.pop("_id", None)

        return SessionModel(**document)

    # =====================================================
    # Update Progress
    # =====================================================

    async def update_progress(
        self,
        db: AsyncIOMotorDatabase,
        session_id: str,
        progress: int,
        current_stage: str,
    ) -> None:
        """
        Update processing progress.
        """

        await db[self.COLLECTION].update_one(
            {
                "session_id": session_id
            },
            {
                "$set": {
                    "progress": progress,
                    "current_stage": current_stage,
                    "updated_at": datetime.utcnow(),
                }
            },
        )

    # =====================================================
    # Update Status
    # =====================================================

    async def update_status(
        self,
        db: AsyncIOMotorDatabase,
        session_id: str,
        status: SessionStatus,
        error_message: str | None = None,
    ) -> None:
        """
        Update session status.
        """

        update = {
            "status": status,
            "updated_at": datetime.utcnow(),
        }

        if status == SessionStatus.COMPLETED:

            update["completed_at"] = datetime.utcnow()

        if error_message:

            update["error_message"] = error_message

        await db[self.COLLECTION].update_one(
            {
                "session_id": session_id
            },
            {
                "$set": update
            },
        )

    # =====================================================
    # Complete Session
    # =====================================================

    async def complete_session(
        self,
        db: AsyncIOMotorDatabase,
        session_id: str,
        image_id: str | None = None,
        analysis_id: str | None = None,
        report_id: str | None = None,
        comparison_id: str | None = None,
        processing_time_seconds: float = 0.0,
    ) -> None:
        """
        Mark session as completed.
        """

        await db[self.COLLECTION].update_one(
            {
                "session_id": session_id
            },
            {
                "$set": {
                    "status": SessionStatus.COMPLETED,
                    "progress": 100,
                    "current_stage": "Completed",
                    "image_id": image_id,
                    "analysis_id": analysis_id,
                    "report_id": report_id,
                    "comparison_id": comparison_id,
                    "processing_time_seconds": processing_time_seconds,
                    "completed_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow(),
                }
            },
        )

    # =====================================================
    # Fail Session
    # =====================================================

    async def fail_session(
        self,
        db: AsyncIOMotorDatabase,
        session_id: str,
        error_message: str,
    ) -> None:
        """
        Mark session as failed.
        """

        await db[self.COLLECTION].update_one(
            {
                "session_id": session_id
            },
            {
                "$set": {
                    "status": SessionStatus.FAILED,
                    "error_message": error_message,
                    "updated_at": datetime.utcnow(),
                }
            },
        )

    # =====================================================
    # Delete Session
    # =====================================================

    async def delete_session(
        self,
        db: AsyncIOMotorDatabase,
        session_id: str,
    ) -> bool:
        """
        Delete a session.
        """

        result = await db[self.COLLECTION].delete_one(
            {
                "session_id": session_id
            }
        )

        return result.deleted_count > 0

    # =====================================================
    # List Sessions
    # =====================================================

    async def list_sessions(
        self,
        db: AsyncIOMotorDatabase,
        limit: int = 20,
    ) -> list[SessionModel]:
        """
        Return recent sessions.
        """

        cursor = (
            db[self.COLLECTION]
            .find()
            .sort(
                "created_at",
                -1,
            )
            .limit(limit)
        )

        sessions = []

        async for document in cursor:

            document.pop("_id", None)

            sessions.append(
                SessionModel(**document)
            )

        return sessions


# ==========================================================
# Singleton
# ==========================================================

session_service = SessionService()