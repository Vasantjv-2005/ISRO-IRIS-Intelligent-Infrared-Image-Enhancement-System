"""
Base Repository

Abstract base class providing common MongoDB repository functionality.
"""

from __future__ import annotations

from abc import ABC
from typing import Any, Generic, List, Type, TypeVar

from motor.motor_asyncio import AsyncIOMotorCollection
from pydantic import BaseModel

from app.database.mongodb import get_database

T = TypeVar("T", bound=BaseModel)


class BaseRepository(ABC, Generic[T]):
    """
    Abstract base repository for MongoDB collections.
    """

    def __init__(self, model_class: Type[T], collection_name: str) -> None:
        self.model_class = model_class
        self.collection_name = collection_name

    @property
    def collection(self) -> AsyncIOMotorCollection:
        """
        Return the MongoDB collection instance.
        """

        db = get_database()

        return db[self.collection_name]

    async def count(self, filter_query: dict[str, Any] | None = None) -> int:
        """
        Count documents matching the query filter.
        """

        query = filter_query or {}

        return await self.collection.count_documents(query)

    async def exists(self, filter_query: dict[str, Any]) -> bool:
        """
        Check if any document matches the query filter.
        """

        count = await self.collection.count_documents(filter_query, limit=1)

        return count > 0

    async def delete_by_filter(self, filter_query: dict[str, Any]) -> bool:
        """
        Delete a single document matching the filter.
        """

        result = await self.collection.delete_one(filter_query)

        return result.deleted_count > 0
