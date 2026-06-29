"""
Preprocessing Routes

Provides API endpoints for image preprocessing.
"""

from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.middleware.error_handler import ImageProcessingException
from app.services.image_processing.contrast_enhancement import (
    contrast_enhancement_service,
)
from app.services.image_processing.crop import (
    crop_service,
)
from app.services.image_processing.noise_reduction import (
    noise_reduction_service,
)
from app.services.image_processing.normalization import (
    normalization_service,
)
from app.services.image_processing.resize import (
    resize_service,
)

router = APIRouter(
    prefix="/preprocessing",
    tags=["Image Preprocessing"],
)


@router.post(
    "/process",
    summary="Run Complete Image Preprocessing Pipeline",
)
async def preprocess_image(
    image_path: str,
):
    """
    Complete preprocessing pipeline.

    Pipeline:

    1. Resize
    2. Normalize
    3. Noise Reduction
    4. Contrast Enhancement
    """

    try:

        image = Path(image_path)

        if not image.exists():
            raise HTTPException(
                status_code=404,
                detail="Image not found.",
            )

        output_directory = image.parent

        resized_path = str(
            output_directory / "resized.jpg"
        )

        normalized_path = str(
            output_directory / "normalized.jpg"
        )

        denoised_path = str(
            output_directory / "denoised.jpg"
        )

        enhanced_path = str(
            output_directory / "enhanced.jpg"
        )

        # ------------------------------------
        # Resize
        # ------------------------------------

        resize_service.resize(
            input_path=image_path,
            output_path=resized_path,
            width=640,
            height=640,
        )

        # ------------------------------------
        # Normalize
        # ------------------------------------

        normalization_service.normalize(
            input_path=resized_path,
            output_path=normalized_path,
        )

        # ------------------------------------
        # Noise Reduction
        # ------------------------------------

        noise_reduction_service.reduce_noise(
            input_path=normalized_path,
            output_path=denoised_path,
        )

        # ------------------------------------
        # Contrast Enhancement
        # ------------------------------------

        contrast_enhancement_service.enhance(
            input_path=denoised_path,
            output_path=enhanced_path,
        )

        return {
            "success": True,
            "message": "Preprocessing completed successfully.",
            "input_image": image_path,
            "output_image": enhanced_path,
        }

    except ImageProcessingException as exc:

        raise HTTPException(
            status_code=500,
            detail=exc.message,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )