"""
Dashboard Routes

API endpoints for retrieving IRIS dashboard statistics.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database.mongodb import get_database
from app.schemas.dashboard_schema import DashboardResponseSchema
from app.services.dashboard.dashboard_service import dashboard_service

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/",
    response_model=DashboardResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Get Dashboard Statistics",
)
async def get_dashboard_statistics(
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> DashboardResponseSchema:
    """
    Retrieve statistics, recent activities, and system health status for the dashboard.
    """
    try:
        stats = await dashboard_service.get_dashboard(db)
        return DashboardResponseSchema(**stats)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load dashboard data: {exc}",
        )
