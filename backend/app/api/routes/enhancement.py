"""
Enhancement Routes

API endpoints for infrared image enhancement.
"""

from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.middleware.error_handler import ImageProcessingException
from app.services.ai.enhancement_service import enhancement_service

router = APIRouter(
    prefix="/enhancement",
    tags=["AI Enhancement"],
)


@router.post(
    "/process",
    summary="Enhance an infrared image",
)
async def enhance_image(
    image_path: str,
):
    """
    Enhance an infrared image.
    """

    try:

        input_image = Path(image_path)

        if not input_image.exists():
            raise HTTPException(
                status_code=404,
                detail="Input image not found.",
            )

        output_directory = input_image.parent

        output_image = str(
            output_directory / "enhanced_ai.jpg"
        )

        enhancement_service.enhance(
            input_path=image_path,
            output_path=output_image,
        )

        return {
            "success": True,
            "message": "Image enhancement completed successfully.",
            "input_image": image_path,
            "enhanced_image": output_image,
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