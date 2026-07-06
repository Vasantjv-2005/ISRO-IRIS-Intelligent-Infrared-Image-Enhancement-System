"""
Dashboard Controller

Handles dashboard statistics requests by delegating to Dashboard Service.
"""

from __future__ import annotations

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.services.dashboard.dashboard_service import dashboard_service


class DashboardController:
    """
    Controller responsible for dashboard operations.
    """

    async def get_dashboard_statistics(
        self,
        db: AsyncIOMotorDatabase,
    ):
        """
        Retrieve statistics and activities for the dashboard.
        """
        return await dashboard_service.get_dashboard(db)


dashboard_controller = DashboardController()
