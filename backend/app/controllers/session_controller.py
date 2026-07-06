"""
Session Controller

Handles image processing session requests by delegating to Session Service.
"""

from __future__ import annotations

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.models.session_model import SessionModel
from app.services.session.session_service import session_service


class SessionController:
    """
    Controller responsible for session management.
    """

    async def create_session(
        self,
        db: AsyncIOMotorDatabase,
        upload_id: str,
    ) -> SessionModel:
        """
        Create a new processing session.
        """
        return await session_service.create_session(db, upload_id)

    async def get_session(
        self,
        db: AsyncIOMotorDatabase,
        session_id: str,
    ) -> SessionModel | None:
        """
        Retrieve session details by ID.
        """
        return await session_service.get_session(db, session_id)

    async def list_sessions(
        self,
        db: AsyncIOMotorDatabase,
        limit: int = 20,
    ) -> list[SessionModel]:
        """
        List recent processing sessions.
        """
        return await session_service.list_sessions(db, limit)

    async def delete_session(
        self,
        db: AsyncIOMotorDatabase,
        session_id: str,
    ) -> bool:
        """
        Delete a processing session.
        """
        return await session_service.delete_session(db, session_id)


session_controller = SessionController()
