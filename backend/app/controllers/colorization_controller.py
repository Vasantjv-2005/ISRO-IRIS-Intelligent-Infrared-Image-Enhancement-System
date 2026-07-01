"""
Colorization Controller

Handles image colorization requests by delegating to ColorizationService.
"""

from __future__ import annotations

import cv2

from app.services.ai.colorization_service import colorization_service


class ColorizationController:
    """
    Controller responsible for image colorization.
    """

    async def colorize(
        self,
        input_path: str,
        output_path: str,
        color_map: int = cv2.COLORMAP_INFERNO,
    ) -> str:
        """
        Colorize an infrared image.
        """
        return colorization_service.colorize(
            input_path=input_path,
            output_path=output_path,
            color_map=color_map,
        )


colorization_controller = ColorizationController()
