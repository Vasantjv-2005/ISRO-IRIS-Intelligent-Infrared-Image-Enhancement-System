"""
Crop Service

Provides image cropping utilities for the IRIS Backend.
"""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from app.middleware.error_handler import ImageProcessingException


class CropService:
    """
    Service responsible for image cropping.
    """

    def crop(
        self,
        input_path: str,
        output_path: str,
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> str:
        """
        Crop an image using the given rectangle.

        Args:
            input_path: Input image path.
            output_path: Output image path.
            x: Starting X coordinate.
            y: Starting Y coordinate.
            width: Crop width.
            height: Crop height.

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

        image_height, image_width = image.shape[:2]

        if (
            x < 0
            or y < 0
            or width <= 0
            or height <= 0
            or x + width > image_width
            or y + height > image_height
        ):
            raise ImageProcessingException(
                "Invalid crop dimensions."
            )

        cropped = image[y:y + height, x:x + width]

        output_file = Path(output_path)

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        success = cv2.imwrite(
            str(output_file),
            cropped,
        )

        if not success:
            raise ImageProcessingException(
                "Failed to save cropped image."
            )

        return str(output_file)

    def center_crop(
        self,
        input_path: str,
        output_path: str,
        crop_width: int,
        crop_height: int,
    ) -> str:
        """
        Crop the center region of an image.

        Args:
            input_path: Input image path.
            output_path: Output image path.
            crop_width: Width of crop.
            crop_height: Height of crop.

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

        image_height, image_width = image.shape[:2]

        if (
            crop_width > image_width
            or crop_height > image_height
        ):
            raise ImageProcessingException(
                "Crop size exceeds image dimensions."
            )

        x = (image_width - crop_width) // 2
        y = (image_height - crop_height) // 2

        return self.crop(
            input_path=input_path,
            output_path=output_path,
            x=x,
            y=y,
            width=crop_width,
            height=crop_height,
        )

    def crop_array(
        self,
        image: np.ndarray,
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> np.ndarray:
        """
        Crop an in-memory image.

        Args:
            image: NumPy image.
            x: Starting X coordinate.
            y: Starting Y coordinate.
            width: Crop width.
            height: Crop height.

        Returns:
            Cropped NumPy image.
        """

        if image is None:
            raise ImageProcessingException(
                "Invalid image supplied."
            )

        image_height, image_width = image.shape[:2]

        if (
            x < 0
            or y < 0
            or width <= 0
            or height <= 0
            or x + width > image_width
            or y + height > image_height
        ):
            raise ImageProcessingException(
                "Invalid crop dimensions."
            )

        return image[y:y + height, x:x + width]


crop_service = CropService()