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
    summary="Colorize an infrared image",
)
async def colorize_image(
    image_path: str,
    colormap: str = "inferno",
):
    """
    Colorize an infrared image. Supports colormaps: inferno, turbo, jet, magma, hot, etc.
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
            output_directory / "colorized.jpg"
        )

        await colorization_controller.colorize(
            input_path=image_path,
            output_path=output_image,
            color_map=colormap,
        )

        return {
            "success": True,
            "message": f"Image colorization completed successfully using {colormap} palette.",
            "input_image": image_path,
            "colorized_image": output_image,
            "colormap_used": colormap,
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