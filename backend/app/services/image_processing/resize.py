"""
Resize Service

Resizes infrared images while preserving aspect ratio.
"""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from app.middleware.error_handler import ImageProcessingException


class ResizeService:
    """
    Service responsible for resizing images.
    """

    def resize(
        self,
        input_path: str,
        output_path: str,
        width: int,
        height: int,
        keep_aspect_ratio: bool = True,
    ) -> str:
        """
        Resize an image.

        Args:
            input_path: Path of the input image.
            output_path: Path where resized image will be saved.
            width: Target width.
            height: Target height.
            keep_aspect_ratio: Preserve aspect ratio.

        Returns:
            Output image path.
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

        if width <= 0 or height <= 0:
            raise ImageProcessingException(
                "Width and height must be greater than zero."
            )

        if keep_aspect_ratio:

            original_height, original_width = image.shape[:2]

            scale = min(
                width / original_width,
                height / original_height,
            )

            new_width = int(original_width * scale)
            new_height = int(original_height * scale)

            resized = cv2.resize(
                image,
                (new_width, new_height),
                interpolation=cv2.INTER_AREA,
            )

        else:

            resized = cv2.resize(
                image,
                (width, height),
                interpolation=cv2.INTER_AREA,
            )

        output_file = Path(output_path)

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        success = cv2.imwrite(
            str(output_file),
            resized,
        )

        if not success:
            raise ImageProcessingException(
                "Failed to save resized image."
            )

        return str(output_file)

    def resize_array(
        self,
        image: np.ndarray,
        width: int,
        height: int,
        keep_aspect_ratio: bool = True,
    ) -> np.ndarray:
        """
        Resize an image already loaded into memory.

        Args:
            image: NumPy image.
            width: Target width.
            height: Target height.
            keep_aspect_ratio: Preserve aspect ratio.

        Returns:
            Resized NumPy image.
        """

        if image is None:
            raise ImageProcessingException(
                "Invalid image supplied."
            )

        if width <= 0 or height <= 0:
            raise ImageProcessingException(
                "Width and height must be greater than zero."
            )

        if keep_aspect_ratio:

            original_height, original_width = image.shape[:2]

            scale = min(
                width / original_width,
                height / original_height,
            )

            width = int(original_width * scale)
            height = int(original_height * scale)

        return cv2.resize(
            image,
            (width, height),
            interpolation=cv2.INTER_AREA,
        )


resize_service = ResizeService()