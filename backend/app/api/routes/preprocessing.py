"""
Preprocessing Routes

API endpoints for image preprocessing.
"""

from fastapi import APIRouter, HTTPException

from app.middleware.error_handler import ImageProcessingException
from app.schemas.preprocessing_schema import (
    PreprocessingRequestSchema,
)
from app.controllers.preprocessing_controller import (
    preprocessing_controller,
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
    request: PreprocessingRequestSchema,
):
    """
    Run the complete preprocessing pipeline.
    """

    try:

        result = await preprocessing_controller.preprocess(request)

        return result

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