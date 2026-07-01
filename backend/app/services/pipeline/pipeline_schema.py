"""
Pipeline Schemas
"""

from pydantic import BaseModel


class PipelineResponseSchema(BaseModel):

    success: bool

    upload_id: str

    processed_image: str

    enhanced_image: str

    colorized_image: str

    detection_count: int

    analysis: str

    report_path: str

    message: str