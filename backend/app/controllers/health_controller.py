"""
Health Controller

Provides backend health status checks.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from app.database.mongodb import get_database


class HealthController:
    """
    Controller responsible for backend health checking.
    """

    async def check_health(self) -> dict[str, Any]:
        """
        Check backend and MongoDB health status.
        """
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


health_controller = HealthController()
