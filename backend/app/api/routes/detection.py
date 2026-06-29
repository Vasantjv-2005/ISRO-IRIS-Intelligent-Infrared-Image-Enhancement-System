"""
Detection Routes

API endpoints for object detection using YOLOv8.
"""

from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.middleware.error_handler import ImageProcessingException
from app.services.ai.detection_service import detection_service

router = APIRouter(
    prefix="/detection",
    tags=["AI Detection"],
)


@router.post(
    "/process",
    summary="Detect objects in an infrared image",
)
async def detect_objects(
    image_path: str,
    confidence: float = 0.25,
):
    """
    Detect objects in an infrared image.
    """

    try:

        input_image = Path(image_path)

        if not input_image.exists():
            raise HTTPException(
                status_code=404,
                detail="Input image not found.",
            )

        output_directory = "outputs/detections"

        result = detection_service.detect(
            image_path=image_path,
            output_directory=output_directory,
            confidence=confidence,
        )

        return {
            "success": True,
            "message": "Object detection completed successfully.",
            "result": result,
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