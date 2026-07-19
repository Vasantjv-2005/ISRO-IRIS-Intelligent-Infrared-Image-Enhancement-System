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

    async def compare_multi_images(
        self,
        db: AsyncIOMotorDatabase,
        upload_id: str,
        enhanced_path: str | None = None,
        colorized_path: str | None = None,
        detected_path: str | None = None,
    ):
        """
        Generate multi-stage comparison image (Enhanced, Colorized, Detected).
        """
        return await comparison_service.generate_multi_comparison(
            db=db,
            upload_id=upload_id,
            enhanced_path=enhanced_path,
            colorized_path=colorized_path,
            detected_path=detected_path,
        )


comparison_controller = ComparisonController()

