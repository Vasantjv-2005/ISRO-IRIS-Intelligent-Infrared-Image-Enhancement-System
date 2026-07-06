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
from app.controllers.analysis_controller import analysis_controller

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

        return await analysis_controller.analyze_scene(request)

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