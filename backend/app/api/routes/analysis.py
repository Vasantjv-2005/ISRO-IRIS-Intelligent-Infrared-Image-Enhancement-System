"""
Analysis Routes

API endpoints for AI scene analysis using Gemini.
"""

from fastapi import APIRouter, HTTPException, status

from app.middleware.error_handler import AIModelException
from app.schemas.analysis_schema import (
    AnalysisRequestSchema,
    AnalysisResponseSchema,
)
from app.services.ai.analysis_service import analysis_service

router = APIRouter(
    prefix="/analysis",
    tags=["AI Analysis"],
)


@router.post(
    "/process",
    response_model=AnalysisResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Analyze detected objects using Gemini AI",
)
async def analyze_scene(
    request: AnalysisRequestSchema,
) -> AnalysisResponseSchema:
    """
    Analyze detected objects using the Gemini AI model.
    """

    try:

        result = analysis_service.analyze(
            image_name=request.image_name,
            detected_objects=[
                detection.model_dump()
                for detection in request.detected_objects
            ],
        )

        return AnalysisResponseSchema(
            success=True,
            image=result["image"],
            analysis=result["analysis"],
            model="Gemini",
            total_detected_objects=len(
                request.detected_objects
            ),
            message="Scene analysis completed successfully.",
        )

    except AIModelException as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=exc.message,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )