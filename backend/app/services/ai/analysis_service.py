"""
AI Enhancement Service

Enhances infrared images using classical image enhancement
techniques. This service is designed so that a deep-learning
model can be integrated later without changing the API.
"""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from app.middleware.error_handler import ImageProcessingException


class EnhancementService:
    """
    Service responsible for infrared image enhancement.
    """

    def enhance(
        self,
        input_path: str,
        output_path: str,
        gamma: float = 1.2,
    ) -> str:
        """
        Enhance an infrared image.

        Args:
            input_path: Path of the input image.
            output_path: Path where enhanced image is saved.
            gamma: Gamma correction factor.

        Returns:
            Path to enhanced image.
        """

        input_file = Path(input_path)

        if not input_file.exists():
            raise ImageProcessingException(
                "Input image does not exist."
            )

        image = cv2.imread(str(input_file))

        if image is None:
            raise ImageProcessingException(
                "Unable to read input image."
            )

        enhanced = self.enhance_array(
            image=image,
            gamma=gamma,
        )

        output_file = Path(output_path)

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        success = cv2.imwrite(
            str(output_file),
            enhanced,
        )

        if not success:
            raise ImageProcessingException(
                "Failed to save enhanced image."
            )

        return str(output_file)

    def enhance_array(
        self,
        image: np.ndarray,
        gamma: float = 1.2,
    ) -> np.ndarray:
        """
        Enhance an image already loaded into memory.

        Args:
            image: NumPy image.
            gamma: Gamma correction value.

        Returns:
            Enhanced image.
        """

        if image is None:
            raise ImageProcessingException(
                "Invalid image supplied."
            )

        # ----------------------------------------
        # Gamma Correction
        # ----------------------------------------

        inverse_gamma = 1.0 / gamma

        table = np.array(
            [
                ((i / 255.0) ** inverse_gamma) * 255
                for i in np.arange(256)
            ]
        ).astype("uint8")

        gamma_corrected = cv2.LUT(
            image,
            table,
        )

        # ----------------------------------------
        # CLAHE Enhancement
        # ----------------------------------------

        lab = cv2.cvtColor(
            gamma_corrected,
            cv2.COLOR_BGR2LAB,
        )

        l_channel, a_channel, b_channel = cv2.split(lab)

        clahe = cv2.createCLAHE(
            clipLimit=2.0,
            tileGridSize=(8, 8),
        )

        enhanced_l = clahe.apply(l_channel)

        merged = cv2.merge(
            (
                enhanced_l,
                a_channel,
                b_channel,
            )
        )

        enhanced = cv2.cvtColor(
            merged,
            cv2.COLOR_LAB2BGR,
        )

        return enhanced


enhancement_service = EnhancementService()