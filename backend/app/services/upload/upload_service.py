"""
Upload Service

Handles the complete upload workflow:
- Validate uploaded image
- Save image to disk
- Extract basic metadata
- Store upload record
- Store image metadata
- Return upload response
"""

from __future__ import annotations

from datetime import datetime

import cv2
from fastapi import UploadFile

from app.models.image_model import ImageModel
from app.models.image_model import (
    ImageModel,
    ImageStatus,
)
from app.schemas.upload_schema import UploadResponseSchema
from app.services.storage.image_storage import image_storage
from app.services.storage.metadata_storage import metadata_storage
from app.services.storage.upload_storage import upload_storage
from app.services.upload.validation_service import validation_service


class UploadService:
    """
    Handles image upload operations.
    """

    async def upload_image(
        self,
        file: UploadFile,
    ) -> UploadResponseSchema:
        """
        Upload an infrared image.

        Workflow:

        1. Validate image
        2. Save image
        3. Extract metadata
        4. Save upload document
        5. Save image document
        6. Return response
        """

        # -------------------------------------------------
        # Validate Upload
        # -------------------------------------------------

        await validation_service.validate(file)

        # -------------------------------------------------
        # Save Image
        # -------------------------------------------------

        (
            original_filename,
            stored_filename,
            file_path,
            file_size,
            mime_type,
        ) = await image_storage.save_image(file)

        # -------------------------------------------------
        # Read Image
        # -------------------------------------------------

        image = cv2.imread(file_path)

        if image is None:
            image_storage.delete_image(file_path)

            raise ValueError(
                "Uploaded image could not be read."
            )

        image_height, image_width = image.shape[:2]

        image_format = stored_filename.split(".")[-1].upper()

        uploaded_at = datetime.utcnow()
        # -------------------------------------------------
        # Create Upload Model
        # -------------------------------------------------

        upload_model = UploadModel(
            filename=stored_filename,
            original_filename=original_filename,
            file_path=file_path,
            file_size=file_size,
            file_type=image_format,
            status=ProcessingStatus.UPLOADED,
            uploaded_at=uploaded_at,
            created_at=uploaded_at,
            updated_at=uploaded_at,
        )

        upload_id = await upload_storage.create_upload(
            upload_model.model_dump()
        )

        # -------------------------------------------------
        # Create Image Model
        # -------------------------------------------------

        image_model = ImageModel(
            upload_id=upload_id,
            original_filename=original_filename,
            stored_filename=stored_filename,
            original_image_path=file_path,
            image_width=image_width,
            image_height=image_height,
            image_format=image_format,
            image_size=file_size,
            mime_type=mime_type,
            status=ImageStatus.UPLOADED,
            created_at=uploaded_at,
            updated_at=uploaded_at,
        )

        await metadata_storage.save_metadata(
            image_model.model_dump()
        )

        # -------------------------------------------------
        # Return Response
        # -------------------------------------------------

        return UploadResponseSchema(
            upload_id=upload_id,
            filename=stored_filename,
            original_filename=original_filename,
            file_path=file_path,
            file_size=file_size,
            file_type=image_format,
            mime_type=mime_type,
            status=ProcessingStatus.UPLOADED,
            uploaded_at=uploaded_at,
            message="Image uploaded successfully.",
               )

    async def get_upload(
        self,
        upload_id: str,
    ):
        """
        Retrieve an upload by its ID.
        """

        return await upload_storage.get_upload(upload_id)

    async def delete_upload(
        self,
        upload_id: str,
    ) -> bool:
        """
        Delete an upload record.

        Note:
            This removes the MongoDB record only.
            Image file deletion can be added later if required.
        """

        return await upload_storage.delete_upload(upload_id)


upload_service = UploadService()