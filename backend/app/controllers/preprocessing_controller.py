"""
Preprocessing Controller

Handles image preprocessing requests by delegating to PreprocessingService.
"""

from __future__ import annotations

from typing import Any

from app.schemas.preprocessing_schema import PreprocessingRequestSchema
from app.services.image_processing.preprocessing_service import (
    preprocessing_service,
)


class PreprocessingController:
    """
    Controller responsible for image preprocessing.
    """

    async def preprocess(
        self,
        request: PreprocessingRequestSchema,
    ) -> dict[str, Any]:
        """
        Run the complete preprocessing pipeline.
        """
        return preprocessing_service.process(
            input_path=request.image_path,
            output_directory=request.output_directory,
            apply_crop=request.apply_crop,
        )


preprocessing_controller = PreprocessingController()
