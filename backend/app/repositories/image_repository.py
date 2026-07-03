"""
Image Repository

Handles database operations related to processed images.
"""

from __future__ import annotations

from typing import List

from motor.motor_asyncio import AsyncIOMotorCollection

from app.database.mongodb import get_database
from app.models.image_model import (
    ImageModel,
    ImageStatus,
    utc_now,
)
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


class ImageRepository:
    """
    Repository responsible for Images collection.
    """

    COLLECTION = "images"

    @property
    def collection(self) -> AsyncIOMotorCollection:
        """
        Return MongoDB images collection.
        """

        db = get_database()

        return db[self.COLLECTION]

    # =====================================================
    # Create
    # =====================================================

    async def create(
        self,
        image: ImageModel,
    ) -> ImageModel:
        """
        Insert a new image document.
        """

        document = image.model_dump()

        await self.collection.insert_one(document)

        logger.info(
            "Image created: %s",
            image.image_id,
        )

        return image

    # =====================================================
    # Find by Image ID
    # =====================================================

    async def get_by_image_id(
        self,
        image_id: str,
    ) -> ImageModel | None:
        """
        Find image by image_id.
        """

        document = await self.collection.find_one(
            {
                "image_id": image_id
            }
        )

        if document is None:
            return None

        document.pop("_id", None)

        return ImageModel(**document)

    # =====================================================
    # Find by Upload ID
    # =====================================================

    async def get_by_upload_id(
        self,
        upload_id: str,
    ) -> ImageModel | None:
        """
        Find image by upload_id.
        """

        document = await self.collection.find_one(
            {
                "upload_id": upload_id
            }
        )

        if document is None:
            return None

        document.pop("_id", None)

        return ImageModel(**document)

    # =====================================================
    # List Images
    # =====================================================

    async def list_images(
        self,
        limit: int = 100,
    ) -> List[ImageModel]:
        """
        Return latest images.
        """

        cursor = (
            self.collection
            .find()
            .sort(
                "created_at",
                -1,
            )
            .limit(limit)
        )

        images: List[ImageModel] = []

        async for document in cursor:

            document.pop("_id", None)

            images.append(
                ImageModel(**document)
            )

        return images

    # =====================================================
    # Update Status
    # =====================================================

    async def update_status(
        self,
        image_id: str,
        status: ImageStatus,
    ) -> bool:
        """
        Update processing status.
        """

        result = await self.collection.update_one(
            {
                "image_id": image_id
            },
            {
                "$set": {
                    "status": status,
                    "updated_at": utc_now(),
                }
            },
        )

        return result.modified_count > 0

    # =====================================================
    # Update Processed Path
    # =====================================================

    async def update_processed_path(
        self,
        image_id: str,
        processed_image_path: str,
        thumbnail_path: str | None = None,
    ) -> bool:
        """
        Update file paths for processed image and thumbnail.
        """

        updates = {
            "processed_image_path": processed_image_path,
            "updated_at": utc_now(),
        }

        if thumbnail_path is not None:
            updates["thumbnail_path"] = thumbnail_path

        result = await self.collection.update_one(
            {
                "image_id": image_id
            },
            {
                "$set": updates
            },
        )

        return result.modified_count > 0

    # =====================================================
    # Update Flags
    # =====================================================

    async def update_flags(
        self,
        image_id: str,
        *,
        preprocessing: bool | None = None,
        enhancement: bool | None = None,
        colorization: bool | None = None,
        detection: bool | None = None,
        analysis: bool | None = None,
        report: bool | None = None,
    ) -> bool:
        """
        Update processing completion stage flags.
        """

        updates = {
            "updated_at": utc_now(),
        }

        if preprocessing is not None:
            updates["preprocessing_completed"] = preprocessing

        if enhancement is not None:
            updates["enhancement_completed"] = enhancement

        if colorization is not None:
            updates["colorization_completed"] = colorization

        if detection is not None:
            updates["detection_completed"] = detection

        if analysis is not None:
            updates["analysis_completed"] = analysis

        if report is not None:
            updates["report_generated"] = report

        result = await self.collection.update_one(
            {
                "image_id": image_id
            },
            {
                "$set": updates
            },
        )

        return result.modified_count > 0

    # =====================================================
    # Delete
    # =====================================================

    async def delete(
        self,
        image_id: str,
    ) -> bool:
        """
        Delete image document.
        """

        result = await self.collection.delete_one(
            {
                "image_id": image_id
            }
        )

        return result.deleted_count > 0

    # =====================================================
    # Exists
    # =====================================================

    async def exists(
        self,
        image_id: str,
    ) -> bool:
        """
        Check if image exists.
        """

        count = await self.collection.count_documents(
            {
                "image_id": image_id
            },
            limit=1,
        )

        return count > 0

    # =====================================================
    # Count
    # =====================================================

    async def count(self) -> int:
        """
        Return total image documents.
        """

        return await self.collection.count_documents({})


# ==========================================================
# Singleton
# ==========================================================

image_repository = ImageRepository()
