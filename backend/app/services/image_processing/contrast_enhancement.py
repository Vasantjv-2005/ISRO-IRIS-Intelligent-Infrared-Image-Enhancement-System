"""
Contrast Enhancement Service

Enhances infrared image contrast using CLAHE
(Contrast Limited Adaptive Histogram Equalization).
"""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from app.middleware.error_handler import ImageProcessingException


class ContrastEnhancementService:
    """
    Service responsible for enhancing image contrast.
    """

    def enhance(
        self,
        input_path: str,
        output_path: str,
        clip_limit: float = 2.0,
        tile_grid_size: tuple[int, int] = (8, 8),
    ) -> str:
        """
        Enhance image contrast using CLAHE.

        Args:
            input_path: Input image path.
            output_path: Output image path.
            clip_limit: CLAHE clip limit.
            tile_grid_size: CLAHE tile size.

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

        # -------------------------------------------------
        # Convert to LAB color space
        # -------------------------------------------------

        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

        l_channel, a_channel, b_channel = cv2.split(lab)

        clahe = cv2.createCLAHE(
            clipLimit=clip_limit,
            tileGridSize=tile_grid_size,
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


contrast_enhancement_service = ContrastEnhancementService()