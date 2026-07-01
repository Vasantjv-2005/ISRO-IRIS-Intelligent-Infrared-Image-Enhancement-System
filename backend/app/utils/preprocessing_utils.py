"""
Preprocessing Utilities

Reusable image preprocessing helper functions.
"""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np


class PreprocessingUtils:
    """
    Utility class containing reusable image
    preprocessing functions.
    """

    # =====================================================
    # Load Image
    # =====================================================

    @staticmethod
    def load_image(
        image_path: str,
        flags: int = cv2.IMREAD_COLOR,
    ) -> np.ndarray:
        """
        Load an image from disk.
        """

        image = cv2.imread(
            image_path,
            flags,
        )

        if image is None:
            raise FileNotFoundError(
                f"Unable to load image: {image_path}"
            )

        return image

    # =====================================================
    # Save Image
    # =====================================================

    @staticmethod
    def save_image(
        image: np.ndarray,
        output_path: str,
    ) -> str:
        """
        Save an image.
        """

        output = Path(output_path)

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        success = cv2.imwrite(
            str(output),
            image,
        )

        if not success:
            raise IOError(
                f"Unable to save image: {output_path}"
            )

        return str(output)

    # =====================================================
    # Resize
    # =====================================================

    @staticmethod
    def resize(
        image: np.ndarray,
        width: int,
        height: int,
    ) -> np.ndarray:
        """
        Resize image.
        """

        return cv2.resize(
            image,
            (width, height),
            interpolation=cv2.INTER_AREA,
        )

    # =====================================================
    # Crop
    # =====================================================

    @staticmethod
    def crop(
        image: np.ndarray,
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> np.ndarray:
        """
        Crop image.
        """

        return image[
            y:y + height,
            x:x + width,
        ]

    # =====================================================
    # Normalize
    # =====================================================

    @staticmethod
    def normalize(
        image: np.ndarray,
    ) -> np.ndarray:
        """
        Normalize pixel values.
        """

        return cv2.normalize(
            image,
            None,
            alpha=0,
            beta=255,
            norm_type=cv2.NORM_MINMAX,
        )

    # =====================================================
    # Gaussian Blur
    # =====================================================

    @staticmethod
    def gaussian_blur(
        image: np.ndarray,
        kernel_size: int = 5,
    ) -> np.ndarray:
        """
        Apply Gaussian blur.
        """

        return cv2.GaussianBlur(
            image,
            (kernel_size, kernel_size),
            0,
        )

    # =====================================================
    # Median Blur
    # =====================================================

    @staticmethod
    def median_blur(
        image: np.ndarray,
        kernel_size: int = 5,
    ) -> np.ndarray:
        """
        Apply median blur.
        """

        return cv2.medianBlur(
            image,
            kernel_size,
        )

    # =====================================================
    # Histogram Equalization
    # =====================================================

    @staticmethod
    def equalize_histogram(
        image: np.ndarray,
    ) -> np.ndarray:
        """
        Equalize grayscale histogram.
        """

        if len(image.shape) == 3:

            image = cv2.cvtColor(
                image,
                cv2.COLOR_BGR2GRAY,
            )

        return cv2.equalizeHist(image)

    # =====================================================
    # CLAHE
    # =====================================================

    @staticmethod
    def clahe(
        image: np.ndarray,
        clip_limit: float = 2.0,
        tile_grid_size: tuple[int, int] = (8, 8),
    ) -> np.ndarray:
        """
        Apply CLAHE.
        """

        if len(image.shape) == 3:

            gray = cv2.cvtColor(
                image,
                cv2.COLOR_BGR2GRAY,
            )

        else:

            gray = image

        clahe = cv2.createCLAHE(
            clipLimit=clip_limit,
            tileGridSize=tile_grid_size,
        )

        return clahe.apply(gray)

    # =====================================================
    # Convert To Gray
    # =====================================================

    @staticmethod
    def to_grayscale(
        image: np.ndarray,
    ) -> np.ndarray:
        """
        Convert BGR image to grayscale.
        """

        if len(image.shape) == 2:
            return image

        return cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY,
        )

    # =====================================================
    # Convert To RGB
    # =====================================================

    @staticmethod
    def to_rgb(
        image: np.ndarray,
    ) -> np.ndarray:
        """
        Convert BGR to RGB.
        """

        return cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB,
        )

    # =====================================================
    # Image Size
    # =====================================================

    @staticmethod
    def image_size(
        image: np.ndarray,
    ) -> tuple[int, int]:
        """
        Return image width and height.
        """

        height, width = image.shape[:2]

        return width, height

    # =====================================================
    # Validate Image
    # =====================================================

    @staticmethod
    def validate_image(
        image: np.ndarray,
    ) -> bool:
        """
        Validate image object.
        """

        return (
            image is not None
            and image.size > 0
        )


preprocessing_utils = PreprocessingUtils()