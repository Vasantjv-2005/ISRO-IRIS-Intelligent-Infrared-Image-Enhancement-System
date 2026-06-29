"""
Analysis Routes

API endpoints for AI scene analysis using Gemini.
"""

from typing import Any

from fastapi import APIRouter, HTTPException

from app.middleware.error_handler import AIModelException
from app.services.ai.analysis_service import analysis_service

router = APIRouter(
    prefix="/analysis",
    tags=["AI Analysis"],
)


@router.post(
    "/process",
    summary="Analyze detected objects using Gemini",
)
async def analyze_scene(
    image_name: str,
    detected_objects: list[dict[str, Any]],
):
    """
    Analyze detected objects using Gemini AI.
    """

    try:

        result = analysis_service.analyze(
            detected_objects=detected_objects,
            image_name=image_name,
        )

        return {
            "success": True,
            "message": "Scene analysis completed successfully.",
            "result": result,
        }

    except AIModelException as exc:

        raise HTTPException(
            status_code=500,
            detail=exc.message,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )