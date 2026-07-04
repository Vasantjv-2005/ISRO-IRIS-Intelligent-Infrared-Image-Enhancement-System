"""
Preprocessing Service

Runs the complete image preprocessing pipeline.
"""

from pathlib import Path

from app.middleware.error_handler import ImageProcessingException
from app.services.image_processing.contrast_enhancement import (
    contrast_enhancement_service,
)
from app.services.image_processing.crop import crop_service
from app.services.image_processing.noise_reduction import (
    noise_reduction_service,
)
from app.services.image_processing.normalization import (
    normalization_service,
)
from app.services.image_processing.resize import resize_service
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


class PreprocessingService:
    """
    Executes the complete preprocessing pipeline.
    """

    def process(
        self,
        input_path: str,
        output_directory: str = "outputs/preprocessing",
        apply_crop: bool = False,
    ) -> dict:
        """
        Run the preprocessing pipeline.

        Args:
            input_path:
                Path to the uploaded image.

            output_directory:
                Directory where processed images will be saved.

            apply_crop:
                Whether to crop the image.

        Returns:
            Dictionary containing output paths.
        """
        try:
            input_file = Path(input_path)
            if not input_file.exists():
                raise ImageProcessingException("Input image does not exist.")

            logger.info("Starting preprocessing pipeline for %s", input_path)
            output_dir = Path(output_directory)
            output_dir.mkdir(parents=True, exist_ok=True)

            # ----------------------------------
            # Resize
            # ----------------------------------
            resized_image = output_dir / "resized.jpg"
            resize_service.resize(
                input_path=str(input_file),
                output_path=str(resized_image),
                width=640,
                height=640,
            )
            current_image = resized_image
            logger.debug("Resized image saved to %s", resized_image)

            # ----------------------------------
            # Normalize
            # ----------------------------------
            normalized_image = output_dir / "normalized.jpg"
            normalization_service.normalize(
                input_path=str(current_image),
                output_path=str(normalized_image),
            )
            current_image = normalized_image
            logger.debug("Normalized image saved to %s", normalized_image)

            # ----------------------------------
            # Noise Reduction
            # ----------------------------------
            denoised_image = output_dir / "denoised.jpg"
            noise_reduction_service.reduce_noise(
                input_path=str(current_image),
                output_path=str(denoised_image),
            )
            current_image = denoised_image
            logger.debug("Denoised image saved to %s", denoised_image)

            # ----------------------------------
            # Contrast Enhancement
            # ----------------------------------
            enhanced_image = output_dir / "enhanced.jpg"
            contrast_enhancement_service.enhance(
                input_path=str(current_image),
                output_path=str(enhanced_image),
            )
            current_image = enhanced_image
            logger.debug("Enhanced image saved to %s", enhanced_image)

            # ----------------------------------
            # Optional Crop
            # ----------------------------------
            cropped_image = None
            if apply_crop:
                cropped_image = output_dir / "cropped.jpg"
                crop_service.crop(
                    input_path=str(current_image),
                    output_path=str(cropped_image),
                )
                current_image = cropped_image
                logger.debug("Cropped image saved to %s", cropped_image)

            logger.info("Preprocessing pipeline completed successfully for %s", input_path)
            return {
                "success": True,
                "message": "Image preprocessing completed successfully.",
                "input_image": str(input_file),
                "output_directory": str(output_dir),
                "processed_image": str(current_image),
                "steps": {
                    "resized": str(resized_image),
                    "normalized": str(normalized_image),
                    "denoised": str(denoised_image),
                    "enhanced": str(enhanced_image),
                    "cropped": str(cropped_image) if apply_crop and cropped_image else None,
                },
            }

        except Exception as exc:
            logger.error("Preprocessing failed for %s: %s", input_path, exc, exc_info=True)
            raise ImageProcessingException(str(exc)) from exc


preprocessing_service = PreprocessingService()