"""
Detection Routes

API endpoints for object detection using YOLOv8.
"""

from fastapi import APIRouter, HTTPException, status

from app.middleware.error_handler import ImageProcessingException
from app.schemas.detection_schema import (
    DetectionRequestSchema,
    DetectionResponseSchema,
)
from app.services.ai.detection_service import detection_service

router = APIRouter(
    prefix="/detection",
    tags=["AI Detection"],
)


@router.post(
    "/process",
    response_model=DetectionResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Detect objects in an image",
)
async def detect_objects(
    request: DetectionRequestSchema,
) -> DetectionResponseSchema:
    """
    Detect objects using the YOLOv8 model.
    """

    try:

        result = detection_service.detect(
            image_path=request.image_path,
            output_directory=request.output_directory,
            confidence=request.confidence,
        )

        return DetectionResponseSchema(
            success=True,
            image_path=result["image_path"],
            output_directory=result["output_directory"],
            total_objects=result["total_objects"],
            detections=result["detections"],
            message="Object detection completed successfully.",
        )

    except ImageProcessingException as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=exc.message,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )