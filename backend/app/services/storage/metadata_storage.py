"""
Metadata Storage Service

Handles storing and retrieving image metadata
from MongoDB.
"""

from datetime import datetime
from typing import Any

from bson import ObjectId

from app.database.mongodb import get_database


class MetadataStorageService:
    """
    Service responsible for metadata storage.
    """

    def __init__(self):
        self.collection_name = "images"

    async def save_metadata(
        self,
        metadata: dict[str, Any],
    ) -> str:
        """
        Save image metadata into MongoDB.

        Returns:
            Document ID
        """

        db = get_database()

        metadata["created_at"] = datetime.utcnow()
        metadata["updated_at"] = datetime.utcnow()

        result = await db[self.collection_name].insert_one(metadata)

        return str(result.inserted_id)

    async def get_metadata(
        self,
        metadata_id: str,
    ) -> dict[str, Any] | None:
        """
        Retrieve metadata by ID.
        """

        db = get_database()

        document = await db[self.collection_name].find_one(
            {
                "_id": ObjectId(metadata_id)
            }
        )

        if document:
            document["_id"] = str(document["_id"])

        return document

    async def update_metadata(
        self,
        metadata_id: str,
        updated_data: dict[str, Any],
    ) -> bool:
        """
        Update existing metadata.
        """

        db = get_database()

        updated_data["updated_at"] = datetime.utcnow()

        result = await db[self.collection_name].update_one(
            {
                "_id": ObjectId(metadata_id)
            },
            {
                "$set": updated_data
            },
        )

        return result.modified_count > 0

    async def delete_metadata(
        self,
        metadata_id: str,
    ) -> bool:
        """
        Delete metadata.
        """

        db = get_database()

        result = await db[self.collection_name].delete_one(
            {
                "_id": ObjectId(metadata_id)
            }
        )

        return result.deleted_count > 0

    async def list_metadata(
        self,
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """
        Return recent metadata.
        """

        db = get_database()

        cursor = (
            db[self.collection_name]
            .find()
            .sort("created_at", -1)
            .limit(limit)
        )

        documents = []

        async for document in cursor:
            document["_id"] = str(document["_id"])
            documents.append(document)

        return documents


metadata_storage = MetadataStorageService()