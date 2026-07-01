"""
AI Enhancement Service

Provides infrared image enhancement by delegating to the unified
EnhancementModel wrapper, supporting both OpenCV and Deep Learning.
"""

from __future__ import annotations

import cv2
import numpy as np

from app.ai_models.enhancement_model import enhancement_model
from app.middleware.error_handler import ImageProcessingException


class EnhancementService:
    """
    Service responsible for infrared image enhancement.
    """

    def enhance(
        self,
        input_path: str,
        output_path: str,
    ) -> str:
        """
        Enhance an infrared image.

        Args:
            input_path: Input image path.
            output_path: Output image path.

        Returns:
            Output image path.
        """
        try:
            return enhancement_model.enhance(
                input_path=input_path,
                output_path=output_path,
            )
        except Exception as exc:
            raise ImageProcessingException(
                f"Failed to enhance image: {exc}"
            ) from exc

    def enhance_array(
        self,
        image: np.ndarray,
    ) -> np.ndarray:
        """
        Enhance an image already loaded into memory.

        Args:
            image: NumPy BGR image.

        Returns:
            Enhanced image.
        """
        try:
            return enhancement_model.enhance_array(image)
        except Exception as exc:
            raise ImageProcessingException(
                f"Failed to enhance image array: {exc}"
            ) from exc


enhancement_service = EnhancementService()
