"""
Comparison Routes

API endpoints for comparing an original infrared image with its processed version.
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database.mongodb import get_database
from app.schemas.comparison_schema import (
    ComparisonRequestSchema,
    MultiComparisonRequestSchema,
    ComparisonResponseSchema,
)
from app.controllers.comparison_controller import comparison_controller

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
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> ComparisonResponseSchema:
    """
    Compare two images and return comparison metrics and visualization path.
    """
    try:
        result = await comparison_controller.compare_images(
            db=db,
            upload_id=request.upload_id,
        )

        return ComparisonResponseSchema(
            upload_id=result.upload_id,
            status=result.status,
            original_image_path=result.original_image_path,
            processed_image_path=result.processed_image_path,
            comparison_image_path=result.comparison_image_path,
            enhancement_applied=result.enhancement_applied,
            colorization_applied=result.colorization_applied,
            object_detection_applied=result.object_detection_applied,
            scene_analysis_applied=result.scene_analysis_applied,
            total_objects=result.total_objects,
            similarity_score=result.similarity_score,
            processing_time_seconds=result.processing_time_seconds,
            created_at=result.created_at,
        )

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Image comparison failed: {exc}",
        )


@router.post(
    "/multi",
    response_model=ComparisonResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Generate multi-stage comparison (Enhanced, Colorized, Detected)",
)
async def compare_multi_images(
    request: MultiComparisonRequestSchema,
    db: AsyncIOMotorDatabase = Depends(get_database),
) -> ComparisonResponseSchema:
    """
    Generate multi-stage comparison across Enhanced, Colorized, and Detected images.
    """
    try:
        result = await comparison_controller.compare_multi_images(
            db=db,
            upload_id=request.upload_id,
            enhanced_path=request.enhanced_image_path,
            colorized_path=request.colorized_image_path,
            detected_path=request.detected_image_path,
        )

        return ComparisonResponseSchema(
            upload_id=result.upload_id,
            status=result.status,
            original_image_path=result.original_image_path,
            processed_image_path=result.processed_image_path,
            comparison_image_path=result.comparison_image_path,
            enhancement_applied=result.enhancement_applied,
            colorization_applied=result.colorization_applied,
            object_detection_applied=result.object_detection_applied,
            scene_analysis_applied=result.scene_analysis_applied,
            total_objects=result.total_objects,
            similarity_score=result.similarity_score,
            processing_time_seconds=result.processing_time_seconds,
            created_at=result.created_at,
        )

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Image comparison failed: {exc}",
        )
