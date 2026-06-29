"""
Noise Reduction Service

Removes noise from infrared images while preserving edges.
"""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from app.middleware.error_handler import ImageProcessingException


class NoiseReductionService:
    """
    Service responsible for image noise reduction.
    """

    def reduce_noise(
        self,
        input_path: str,
        output_path: str,
        strength: int = 10,
    ) -> str:
        """
        Reduce image noise.

        Args:
            input_path: Input image path.
            output_path: Output image path.
            strength: Denoising strength.

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
            cv2.IMREAD_COLOR,
        )

        if image is None:
            raise ImageProcessingException(
                "Unable to read input image."
            )

        denoised = cv2.fastNlMeansDenoisingColored(
            image,
            None,
            h=strength,
            hColor=strength,
            templateWindowSize=7,
            searchWindowSize=21,
        )

        output_file = Path(output_path)

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        success = cv2.imwrite(
            str(output_file),
            denoised,
        )

        if not success:
            raise ImageProcessingException(
                "Failed to save denoised image."
            )

        return str(output_file)

    def reduce_noise_array(
        self,
        image: np.ndarray,
        strength: int = 10,
    ) -> np.ndarray:
        """
        Reduce noise for an in-memory image.

        Args:
            image: NumPy image.
            strength: Denoising strength.

        Returns:
            Denoised image.
        """

        if image is None:
            raise ImageProcessingException(
                "Invalid image supplied."
            )

        return cv2.fastNlMeansDenoisingColored(
            image,
            None,
            h=strength,
            hColor=strength,
            templateWindowSize=7,
            searchWindowSize=21,
        )


noise_reduction_service = NoiseReductionService()