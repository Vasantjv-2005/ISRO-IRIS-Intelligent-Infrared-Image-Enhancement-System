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


class ColorizationService:
    """
    Service responsible for infrared image colorization.
    """

    def colorize(
        self,
        input_path: str,
        output_path: str,
        color_map: int = cv2.COLORMAP_INFERNO,
    ) -> str:
        """
        Colorize an infrared image.

        Args:
            input_path: Input image path.
            output_path: Output image path.
            color_map: OpenCV color map.

        Returns:
            Output image path.
        """
        try:
            return colorization_model.colorize(
                input_path=input_path,
                output_path=output_path,
                color_map=color_map,
            )
        except Exception as exc:
            raise ImageProcessingException(
                f"Failed to colorize image: {exc}"
            ) from exc

    def colorize_array(
        self,
        image: np.ndarray,
        color_map: int = cv2.COLORMAP_INFERNO,
    ) -> np.ndarray:
        """
        Colorize an image already loaded into memory.

        Args:
            image: NumPy image.
            color_map: OpenCV color map.

        Returns:
            Colorized image.
        """
        try:
            return colorization_model.colorize_array(
                image=image,
                color_map=color_map,
            )
        except Exception as exc:
            raise ImageProcessingException(
                f"Failed to colorize image array: {exc}"
            ) from exc


colorization_service = ColorizationService()