"""
AI Enhancement Service

Provides infrared image enhancement.

This implementation uses OpenCV-based image processing algorithms
and is designed to be easily replaced by a deep-learning enhancement model.
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
    ) -> str:
        """
        Enhance an infrared image.

        Args:
            input_path: Input image path.
            output_path: Output image path.

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

        enhanced = self.enhance_array(image)

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
    ) -> np.ndarray:
        """
        Enhance an image already loaded into memory.

        Args:
            image: NumPy BGR image.

        Returns:
            Enhanced image.
        """
        if image is None:
            raise ImageProcessingException(
                "Invalid image supplied."
            )

        try:
            # Check if color or grayscale
            is_color = len(image.shape) == 3 and image.shape[2] == 3

            if is_color:
                # Convert to LAB color space
                lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
                l_channel, a_channel, b_channel = cv2.split(lab)

                # Denoise the L channel using Bilateral filter
                denoised_l = cv2.bilateralFilter(
                    l_channel, d=9, sigmaColor=75, sigmaSpace=75
                )

                # Apply CLAHE to the L channel
                clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
                enhanced_l = clahe.apply(denoised_l)

                # Merge back
                merged = cv2.merge((enhanced_l, a_channel, b_channel))
                enhanced = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)
            else:
                # Grayscale image
                denoised = cv2.bilateralFilter(
                    image, d=9, sigmaColor=75, sigmaSpace=75
                )
                clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
                enhanced = clahe.apply(denoised)

            # Apply detail enhancement/sharpening using unsharp masking
            gaussian = cv2.GaussianBlur(enhanced, (5, 5), 1.0)
            sharpened = cv2.addWeighted(enhanced, 1.5, gaussian, -0.5, 0)

            return sharpened

        except Exception as exc:
            raise ImageProcessingException(
                f"Failed to enhance image array: {exc}"
            )


enhancement_service = EnhancementService()
