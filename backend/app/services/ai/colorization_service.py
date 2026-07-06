"""
AI Colorization Service

Provides infrared image colorization by delegating to the unified
ColorizationModel wrapper, supporting both OpenCV and Deep Learning.
"""

from __future__ import annotations

import cv2
import numpy as np

from app.ai_models.colorization_model import colorization_model
from app.middleware.error_handler import ImageProcessingException
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)

COLORMAP_NAMES = {
    "inferno": cv2.COLORMAP_INFERNO,
    "magma": cv2.COLORMAP_MAGMA,
    "plasma": cv2.COLORMAP_PLASMA,
    "hot": cv2.COLORMAP_HOT,
    "turbo": cv2.COLORMAP_TURBO,
    "jet": cv2.COLORMAP_JET,
    "rainbow": cv2.COLORMAP_RAINBOW,
    "ocean": cv2.COLORMAP_OCEAN,
    "twilight": cv2.COLORMAP_TWILIGHT,
    "bone": cv2.COLORMAP_BONE,
    "autumn": cv2.COLORMAP_AUTUMN,
    "spring": cv2.COLORMAP_SPRING,
    "summer": cv2.COLORMAP_SUMMER,
    "winter": cv2.COLORMAP_WINTER,
    "cool": cv2.COLORMAP_COOL,
    "pink": cv2.COLORMAP_PINK,
}


def resolve_colormap(color_map: int | str) -> int:
    """Resolve colormap name or integer to OpenCV COLORMAP constant."""
    if isinstance(color_map, str):
        return COLORMAP_NAMES.get(color_map.lower().strip(), cv2.COLORMAP_INFERNO)
    return color_map


class ColorizationService:
    """
    Service responsible for infrared image colorization.
    """

    def colorize(
        self,
        input_path: str,
        output_path: str,
        color_map: int | str = cv2.COLORMAP_INFERNO,
    ) -> str:
        """
        Colorize an infrared image.

        Args:
            input_path: Input image path.
            output_path: Output image path.
            color_map: OpenCV color map integer or name string.

        Returns:
            Output image path.
        """
        try:
            resolved_map = resolve_colormap(color_map)
            logger.info("Colorizing image from %s to %s with colormap %s (%s)", input_path, output_path, color_map, resolved_map)
            res = colorization_model.colorize(
                input_path=input_path,
                output_path=output_path,
                color_map=resolved_map,
            )
            logger.info("Successfully colorized image: %s", output_path)
            return res
        except Exception as exc:
            logger.error("Failed to colorize image %s: %s", input_path, exc, exc_info=True)
            raise ImageProcessingException(f"Failed to colorize image: {exc}") from exc

    def colorize_array(
        self,
        image: np.ndarray,
        color_map: int | str = cv2.COLORMAP_INFERNO,
    ) -> np.ndarray:
        """
        Colorize an image already loaded into memory.

        Args:
            image: NumPy image.
            color_map: OpenCV color map integer or name string.

        Returns:
            Colorized image.
        """
        try:
            resolved_map = resolve_colormap(color_map)
            return colorization_model.colorize_array(
                image=image,
                color_map=resolved_map,
            )
        except Exception as exc:
            logger.error("Failed to colorize image array: %s", exc, exc_info=True)
            raise ImageProcessingException(f"Failed to colorize image array: {exc}") from exc


colorization_service = ColorizationService()