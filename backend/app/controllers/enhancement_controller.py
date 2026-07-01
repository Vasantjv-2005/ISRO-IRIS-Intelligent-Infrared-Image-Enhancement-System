"""
Enhancement Controller

Handles image enhancement requests by delegating to EnhancementService.
"""

from __future__ import annotations

from app.services.ai.enhancement_service import enhancement_service


class EnhancementController:
    """
    Controller responsible for image enhancement.
    """

    async def enhance(
        self,
        input_path: str,
        output_path: str,
    ) -> str:
        """
        Enhance an infrared image.
        """
        return enhancement_service.enhance(
            input_path=input_path,
            output_path=output_path,
        )


enhancement_controller = EnhancementController()
