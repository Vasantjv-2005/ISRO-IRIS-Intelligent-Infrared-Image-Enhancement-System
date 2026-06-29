"""
MongoDB Database Configuration

This module is responsible for:
- Connecting to MongoDB Atlas
- Providing a database instance
- Closing the database connection gracefully
"""

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
)

from app.core.settings import settings


class MongoDB:
    """
    MongoDB Connection Manager.
    """

    def __init__(self) -> None:
        self.client: AsyncIOMotorClient | None = None
        self.database: AsyncIOMotorDatabase | None = None

    async def connect(self) -> None:
        """
        Connect to MongoDB Atlas.
        """

        if self.client is not None:
            return

        self.client = AsyncIOMotorClient(settings.MONGODB_URI)

        self.database = self.client[settings.DATABASE_NAME]

        print("Connected to MongoDB Atlas")

    async def disconnect(self) -> None:
        """
        Close MongoDB connection.
        """

        if self.client is not None:
            self.client.close()

            self.client = None
            self.database = None

            print("MongoDB Connection Closed")


mongodb = MongoDB()


def get_database() -> AsyncIOMotorDatabase:
    """
    Return the active MongoDB database instance.
    """

    if mongodb.database is None:
        raise RuntimeError(
            "MongoDB has not been connected. "
            "Call mongodb.connect() before accessing the database."
        )

    return mongodb.database