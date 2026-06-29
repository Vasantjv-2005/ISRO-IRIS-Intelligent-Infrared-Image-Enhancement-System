"""
AI Colorization Service

Provides infrared image colorization.

This implementation uses OpenCV color mapping and is designed
to be easily replaced by a deep-learning colorization model.
"""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

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

        input_file = Path(input_path)

        if not input_file.exists():
            raise ImageProcessingException(
                "Input image does not exist."
            )

        image = cv2.imread(
            str(input_file),
            cv2.IMREAD_GRAYSCALE,
        )

        if image is None:
            raise ImageProcessingException(
                "Unable to read input image."
            )

        colorized = self.colorize_array(
            image=image,
            color_map=color_map,
        )

        output_file = Path(output_path)

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        success = cv2.imwrite(
            str(output_file),
            colorized,
        )

        if not success:
            raise ImageProcessingException(
                "Failed to save colorized image."
            )

        return str(output_file)

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

        if image is None:
            raise ImageProcessingException(
                "Invalid image supplied."
            )

        if len(image.shape) == 3:
            image = cv2.cvtColor(
                image,
                cv2.COLOR_BGR2GRAY,
            )

        normalized = cv2.normalize(
            image,
            None,
            0,
            255,
            cv2.NORM_MINMAX,
        )

        colorized = cv2.applyColorMap(
            normalized,
            color_map,
        )

        return colorized


colorization_service = ColorizationService()