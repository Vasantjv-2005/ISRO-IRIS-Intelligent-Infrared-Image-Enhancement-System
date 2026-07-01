"""
Preprocessing Schemas
"""

from pydantic import BaseModel, Field


class PreprocessingRequestSchema(BaseModel):
    """
    Image preprocessing request.
    """

    image_path: str = Field(
        ...,
        description="Path to the input image.",
    )

    output_directory: str = Field(
        default="outputs/preprocessing",
        description="Directory where processed images will be saved.",
    )

    apply_crop: bool = Field(
        default=False,
        description="Whether to crop the image.",
    )