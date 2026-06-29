"""
Upload Storage Service

Handles storing and retrieving upload records
from the MongoDB uploads collection.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from bson import ObjectId
from pymongo.errors import PyMongoError

from app.database.mongodb import get_database
from app.middleware.error_handler import DatabaseException


class UploadStorageService:
    """
    Service responsible for upload document storage.
    """

    @property
    def collection(self):
        """
        Return the uploads collection.
        """

        return get_database()["uploads"]

    async def create_upload(
        self,
        upload_data: dict[str, Any],
    ) -> str:
        """
        Create a new upload document.

        Returns:
            MongoDB document ID.
        """

        try:
            document = upload_data.copy()

            document["created_at"] = datetime.utcnow()
            document["updated_at"] = datetime.utcnow()

            result = await self.collection.insert_one(document)

            return str(result.inserted_id)

        except PyMongoError as exc:
            raise DatabaseException(
                f"Failed to create upload: {exc}"
            ) from exc

    async def get_upload(
        self,
        upload_id: str,
    ) -> dict[str, Any] | None:
        """
        Retrieve upload document by ID.
        """

        try:
            document = await self.collection.find_one(
                {
                    "_id": ObjectId(upload_id)
                }
            )

            if document:
                document["_id"] = str(document["_id"])

            return document

        except PyMongoError as exc:
            raise DatabaseException(
                f"Failed to retrieve upload: {exc}"
            ) from exc

    async def update_upload(
        self,
        upload_id: str,
        updated_data: dict[str, Any],
    ) -> bool:
        """
        Update upload document.
        """

        try:
            document = updated_data.copy()
            document["updated_at"] = datetime.utcnow()

            result = await self.collection.update_one(
                {
                    "_id": ObjectId(upload_id)
                },
                {
                    "$set": document
                },
            )

            return result.modified_count > 0

        except PyMongoError as exc:
            raise DatabaseException(
                f"Failed to update upload: {exc}"
            ) from exc

    async def delete_upload(
        self,
        upload_id: str,
    ) -> bool:
        """
        Delete upload document.
        """

        try:
            result = await self.collection.delete_one(
                {
                    "_id": ObjectId(upload_id)
                }
            )

            return result.deleted_count > 0

        except PyMongoError as exc:
            raise DatabaseException(
                f"Failed to delete upload: {exc}"
            ) from exc

    async def get_by_filename(
        self,
        filename: str,
    ) -> dict[str, Any] | None:
        """
        Retrieve upload document by stored filename.
        """

        try:
            document = await self.collection.find_one(
                {
                    "filename": filename
                }
            )

            if document:
                document["_id"] = str(document["_id"])

            return document

        except PyMongoError as exc:
            raise DatabaseException(
                f"Failed to retrieve upload: {exc}"
            ) from exc


upload_storage = UploadStorageService()