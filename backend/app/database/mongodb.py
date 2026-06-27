"""
MongoDB Database Configuration

This module is responsible for:
- Connecting to MongoDB Atlas
- Providing a database instance
- Closing the database connection gracefully
"""

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.settings import settings


class MongoDB:
    """
    MongoDB Connection Manager
    """

    client: AsyncIOMotorClient | None = None
    database: AsyncIOMotorDatabase | None = None

    async def connect(self) -> None:
        """
        Connect to MongoDB Atlas
        """
        self.client = AsyncIOMotorClient(settings.MONGODB_URI)

        self.database = self.client[settings.DATABASE_NAME]

        print("✅ Connected to MongoDB Atlas")

    async def disconnect(self) -> None:
        """
        Close MongoDB Connection
        """
        if self.client:
            self.client.close()
            print("❌ MongoDB Connection Closed")


mongodb = MongoDB()