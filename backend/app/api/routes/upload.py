"""
Upload Routes

API endpoints for image uploads.
"""

from fastapi import (
    APIRouter,
    File,
    UploadFile,
)

from app.schemas.upload_schema import UploadResponseSchema
from app.services.upload.upload_service import upload_service

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)


@router.post(
    "/",
    response_model=UploadResponseSchema,
    summary="Upload an infrared image",
)
async def upload_image(
    file: UploadFile = File(...),
):
    """
    Upload an infrared image.
    """

    return await upload_service.upload_image(file)