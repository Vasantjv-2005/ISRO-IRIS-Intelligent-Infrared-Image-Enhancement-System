"""
Colorization Controller

Handles image colorization requests by delegating to ColorizationService.
"""

from __future__ import annotations

from typing import Any

import cv2

from app.services.ai.colorization_service import colorization_service


class ColorizationController:
    """
    Controller responsible for image colorization.
    """

    async def colorize_pipeline(
        self,
        input_path: str,
        output_path: str | None = None,
        color_map: int | str = cv2.COLORMAP_INFERNO,
        super_resolution: bool = True,
        backend: str | None = None,
    ) -> dict[str, Any]:
        """
        Run the full 10-stage AI colorization pipeline and return structured metadata.
        """
        return colorization_service.colorize_pipeline(
            input_path=input_path,
            output_path=output_path,
            color_map=color_map,
            super_resolution=super_resolution,
            backend=backend,
        )

    async def colorize(
        self,
        input_path: str,
        output_path: str,
        color_map: int | str = cv2.COLORMAP_INFERNO,
    ) -> str:
        """
        Colorize an infrared image (Backwards-compatible API).
        """
        return colorization_service.colorize(
            input_path=input_path,
            output_path=output_path,
            color_map=color_map,
        )


colorization_controller = ColorizationController()
