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
from app.controllers.detection_controller import detection_controller

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

        result = await detection_controller.detect(
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


@router.post(
    "/save",
    status_code=status.HTTP_200_OK,
    summary="Save detected image to detections folder and MongoDB",
)
async def save_detected_image(payload: dict) -> dict:
    """
    Save detected image and detections list to detections folder and MongoDB database.
    """
    from datetime import datetime
    from pathlib import Path
    from app.database.mongodb import get_database

    try:
        output_dir = Path("outputs/detections")
        output_dir.mkdir(parents=True, exist_ok=True)

        filename = payload.get("filename", "yolo_detection_overlay.jpg")
        image_path = payload.get("image_path", "")
        detections = payload.get("detections", [])

        # Copy or write file to outputs/detections/
        dest_file = output_dir / filename
        if image_path and Path(image_path).exists() and Path(image_path) != dest_file:
            import shutil
            shutil.copy2(image_path, dest_file)

        record = {
            "filename": filename,
            "saved_path": str(dest_file),
            "detections": detections,
            "total_objects": len(detections),
            "saved_at": datetime.utcnow().isoformat(),
            "status": "SAVED_TO_DETECTIONS_FOLDER_AND_MONGODB",
        }

        try:
            db = get_database()
            await db["saved_detections"].insert_one(record)
        except Exception as db_exc:
            print(f"MongoDB save info: {db_exc}")

        return {
            "success": True,
            "saved_path": str(dest_file),
            "message": "Saved detected image to detections folder and MongoDB successfully.",
        }
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save detection: {exc}",
        )