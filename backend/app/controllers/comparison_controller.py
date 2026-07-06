"""
Comparison Controller

Handles image comparison requests by delegating to Comparison Service.
"""

from __future__ import annotations

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.services.dashboard.comparison_service import comparison_service


class ComparisonController:
    """
    Controller responsible for image comparison operations.
    """

    async def compare_images(
        self,
        db: AsyncIOMotorDatabase,
        upload_id: str,
    ):
        """
        Compare original and processed images.
        """
        return await comparison_service.compare(
            db=db,
            upload_id=upload_id,
        )


comparison_controller = ComparisonController()
