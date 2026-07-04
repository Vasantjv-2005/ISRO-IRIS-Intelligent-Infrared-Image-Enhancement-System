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
from uuid import uuid4

import cv2
from fastapi import UploadFile

from app.models.image_model import (
    ImageModel,
    ImageStatus,
)
from app.models.upload_model import (
    ProcessingStatus,
    UploadModel,
    utc_now,
)
from app.repositories.image_repository import image_repository
from app.repositories.upload_repository import upload_repository
from app.schemas.upload_schema import UploadResponseSchema
from app.services.storage.image_storage import image_storage
from app.services.upload.validation_service import validation_service
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


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

        logger.info("Starting image upload validation for file: %s", file.filename)
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

        logger.debug("Saved image to disk: %s (%d bytes)", stored_filename, file_size)

        # -------------------------------------------------
        # Read Image
        # -------------------------------------------------

        image = cv2.imread(file_path)

        if image is None:
            logger.error("Failed to read image with OpenCV: %s", file_path)
            image_storage.delete_image(file_path)

            raise ValueError(
                "Uploaded image could not be read."
            )

        image_height, image_width = image.shape[:2]

        image_format = stored_filename.split(".")[-1].upper()

        uploaded_at = utc_now()
        upload_id = str(uuid4())

        # -------------------------------------------------
        # Create Upload Model
        # -------------------------------------------------

        upload_model = UploadModel(
            upload_id=upload_id,
            filename=stored_filename,
            original_filename=original_filename,
            file_path=file_path,
            file_size=file_size,
            file_type=image_format,
            mime_type=mime_type,
            status=ProcessingStatus.UPLOADED,
            uploaded_at=uploaded_at,
            created_at=uploaded_at,
            updated_at=uploaded_at,
        )

        await upload_repository.create(upload_model)
        logger.info("Created upload document in repository: %s", upload_id)

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

        await image_repository.create(image_model)
        logger.info("Created image document in repository for upload_id: %s", upload_id)

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
    ) -> UploadModel | None:
        """
        Retrieve an upload by its ID.
        """

        logger.debug("Retrieving upload by ID: %s", upload_id)
        return await upload_repository.get_by_upload_id(upload_id)

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

        logger.info("Deleting upload record: %s", upload_id)

        image = await image_repository.get_by_upload_id(upload_id)
        if image:
            await image_repository.delete(image.image_id)
            logger.debug("Deleted associated image metadata for image_id: %s", image.image_id)

        return await upload_repository.delete(upload_id)


upload_service = UploadService()