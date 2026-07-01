"""
Session Routes

API endpoints for managing image processing sessions.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database.mongodb import get_database
from app.models.session_model import SessionModel
from app.services.session.session_service import session_service

router = APIRouter(
    prefix="/sessions",
    tags=["Sessions"],
)


@router.post(
    "/",
    response_model=SessionModel,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new processing session",
)
async def create_session(
    upload_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> SessionModel:
    """
    Create a new processing session for an uploaded image.
    """
    try:
        return await session_service.create_session(db, upload_id)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create session: {exc}",
        )


@router.get(
    "/{session_id}",
    response_model=SessionModel,
    summary="Get session details",
)
async def get_session(
    session_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> SessionModel:
    """
    Retrieve details of a processing session by ID.
    """
    session = await session_service.get_session(db, session_id)
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with ID {session_id} not found.",
        )
    return session


@router.get(
    "/",
    response_model=list[SessionModel],
    summary="List recent sessions",
)
async def list_sessions(
    limit: int = 20,
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> list[SessionModel]:
    """
    List recent processing sessions.
    """
    try:
        return await session_service.list_sessions(db, limit)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list sessions: {exc}",
        )


@router.delete(
    "/{session_id}",
    summary="Delete a session",
)
async def delete_session(
    session_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database),
):
    """
    Delete a processing session.
    """
    success = await session_service.delete_session(db, session_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session with ID {session_id} not found or could not be deleted.",
        )
    return {"success": True, "message": "Session deleted successfully."}
