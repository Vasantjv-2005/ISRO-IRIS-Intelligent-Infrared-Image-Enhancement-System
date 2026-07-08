"""
Colorization Routes

API endpoints for infrared image colorization.
"""

from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.middleware.error_handler import ImageProcessingException
from app.controllers.colorization_controller import (
    colorization_controller,
)

router = APIRouter(
    prefix="/colorization",
    tags=["AI Colorization"],
)


@router.post(
    "/process",
    summary="Colorize an infrared or grayscale image using deep AI colorization",
)
async def colorize_image(
    image_path: str,
    colormap: str = "inferno",
    super_resolution: bool = True,
    backend: str | None = None,
):
    """
    Convert an infrared or grayscale image into a realistic natural daylight RGB photograph.
    Supports AI backends: huggingface, deoldify, palette, torchvision, stablediffusion, deep_learning.
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
            output_directory / f"{input_image.stem}_colorized.jpg"
        )

        result = await colorization_controller.colorize_pipeline(
            input_path=image_path,
            output_path=output_image,
            color_map=colormap,
            super_resolution=super_resolution,
            backend=backend,
        )

        return {
            "success": result["success"],
            "backend": result["backend"],
            "input_image": result["input_image"],
            "output_image": result["output_image"],
            "colorized_image": result["output_image"],  # Backwards compatibility
            "processing_time": result["processing_time"],
            "message": result["message"],
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