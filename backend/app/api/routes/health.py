"""
Health Routes

Provides health check endpoints for the IRIS Backend.
"""

from datetime import datetime

from fastapi import APIRouter, HTTPException

from app.database.mongodb import get_database

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get(
    "/",
    summary="Health Check",
)
async def health_check():
    """
    Check whether the backend and MongoDB are healthy.
    """

    try:
        db = get_database()

        # Ping MongoDB
        await db.command("ping")

        return {
            "success": True,
            "status": "healthy",
            "project": "IRIS",
            "version": "1.0.0",
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "message": "IRIS Backend is running successfully.",
        }

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail={
                "success": False,
                "status": "unhealthy",
                "database": "disconnected",
                "message": str(exc),
            },
        )