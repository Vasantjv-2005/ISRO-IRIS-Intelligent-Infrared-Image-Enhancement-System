"""
Normalization Service

Normalizes infrared images for AI preprocessing.
"""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from app.middleware.error_handler import ImageProcessingException


class NormalizationService:
    """
    Service responsible for image normalization.
    """

    def normalize(
        self,
        input_path: str,
        output_path: str,
    ) -> str:
        """
        Normalize an image using Min-Max normalization.

        Args:
            input_path: Input image path.
            output_path: Output image path.

        Returns:
            Path to normalized image.
        """

        input_file = Path(input_path)

        if not input_file.exists():
            raise ImageProcessingException(
                "Input image does not exist."
            )

        image = cv2.imread(
            str(input_file),
            cv2.IMREAD_UNCHANGED,
        )

        if image is None:
            raise ImageProcessingException(
                "Unable to read input image."
            )

        normalized = cv2.normalize(
            image,
            None,
            alpha=0,
            beta=255,
            norm_type=cv2.NORM_MINMAX,
            dtype=cv2.CV_8U,
        )

        output_file = Path(output_path)

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        success = cv2.imwrite(
            str(output_file),
            normalized,
        )

        if not success:
            raise ImageProcessingException(
                "Failed to save normalized image."
            )

        return str(output_file)

    def normalize_array(
        self,
        image: np.ndarray,
    ) -> np.ndarray:
        """
        Normalize an image array without saving it.

        Args:
            image: Input NumPy image.

        Returns:
            Normalized NumPy image.
        """

        if image is None:
            raise ImageProcessingException(
                "Invalid image supplied."
            )

        return cv2.normalize(
            image,
            None,
            alpha=0,
            beta=255,
            norm_type=cv2.NORM_MINMAX,
            dtype=cv2.CV_8U,
        )


normalization_service = NormalizationService()