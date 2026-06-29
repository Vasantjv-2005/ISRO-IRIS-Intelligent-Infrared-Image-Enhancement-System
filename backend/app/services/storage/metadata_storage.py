"""
Metadata Storage Service

Handles storing, retrieving, updating, and deleting
image metadata in MongoDB.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from bson import ObjectId
from pymongo.errors import PyMongoError

from app.database.mongodb import get_database
from app.middleware.error_handler import DatabaseException


class MetadataStorageService:
    """
    Service responsible for image metadata storage.
    """

    @property
    def collection(self):
        """
        Return the images collection.
        """

        return get_database()["images"]

    async def save_metadata(
        self,
        metadata: dict[str, Any],
    ) -> str:
        """
        Save image metadata.

        Returns:
            MongoDB document ID.
        """

        try:
            document = metadata.copy()

            document["created_at"] = datetime.utcnow()
            document["updated_at"] = datetime.utcnow()

            result = await self.collection.insert_one(document)

            return str(result.inserted_id)

        except PyMongoError as exc:
            raise DatabaseException(
                f"Failed to save metadata: {exc}"
            ) from exc

    async def get_metadata(
        self,
        metadata_id: str,
    ) -> dict[str, Any] | None:
        """
        Retrieve metadata by MongoDB ID.
        """

        try:
            document = await self.collection.find_one(
                {
                    "_id": ObjectId(metadata_id)
                }
            )

            if document:
                document["_id"] = str(document["_id"])

            return document

        except PyMongoError as exc:
            raise DatabaseException(
                f"Failed to retrieve metadata: {exc}"
            ) from exc

    async def update_metadata(
        self,
        metadata_id: str,
        updated_data: dict[str, Any],
    ) -> bool:
        """
        Update metadata.
        """

        try:
            updated_data = updated_data.copy()
            updated_data["updated_at"] = datetime.utcnow()

            result = await self.collection.update_one(
                {
                    "_id": ObjectId(metadata_id)
                },
                {
                    "$set": updated_data
                },
            )

            return result.modified_count > 0

        except PyMongoError as exc:
            raise DatabaseException(
                f"Failed to update metadata: {exc}"
            ) from exc

    async def delete_metadata(
        self,
        metadata_id: str,
    ) -> bool:
        """
        Delete metadata.
        """

        try:
            result = await self.collection.delete_one(
                {
                    "_id": ObjectId(metadata_id)
                }
            )

            return result.deleted_count > 0

        except PyMongoError as exc:
            raise DatabaseException(
                f"Failed to delete metadata: {exc}"
            ) from exc

    async def get_by_upload_id(
        self,
        upload_id: str,
    ) -> dict[str, Any] | None:
        """
        Retrieve metadata using upload ID.
        """

        try:
            document = await self.collection.find_one(
                {
                    "upload_id": upload_id
                }
            )

            if document:
                document["_id"] = str(document["_id"])

            return document

        except PyMongoError as exc:
            raise DatabaseException(
                f"Failed to retrieve metadata: {exc}"
            ) from exc


metadata_storage = MetadataStorageService()