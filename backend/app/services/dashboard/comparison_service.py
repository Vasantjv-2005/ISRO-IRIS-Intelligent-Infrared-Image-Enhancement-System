"""
Comparison Routes

API endpoints for comparing an original image
with a processed image.
"""

from fastapi import APIRouter, HTTPException, status

from app.schemas.comparison_schema import (
    ComparisonRequestSchema,
    ComparisonResponseSchema,
)
from app.services.dashboard.comparison_service import (
    comparison_service,
)

router = APIRouter(
    prefix="/comparison",
    tags=["Image Comparison"],
)


@router.post(
    "/compare",
    response_model=ComparisonResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Compare original and processed images",
)
async def compare_images(
    request: ComparisonRequestSchema,
) -> ComparisonResponseSchema:
    """
    Compare two images and return comparison metrics.
    """

    try:

        result = comparison_service.compare(
            original_path=request.original_image,
            processed_path=request.processed_image,
        )

        return ComparisonResponseSchema(
            success=result["success"],
            original_image=result["original_image"],
            processed_image=result["processed_image"],
            mean_difference=result["mean_difference"],
            mse=result["mse"],
            message="Image comparison completed successfully.",
        )

    except FileNotFoundError as exc:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )