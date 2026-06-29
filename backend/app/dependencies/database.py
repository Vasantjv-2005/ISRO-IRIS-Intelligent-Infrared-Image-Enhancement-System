"""
Database Dependencies

Provides reusable MongoDB dependencies
for FastAPI routes and services.
"""

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database.mongodb import get_database


def get_db() -> AsyncIOMotorDatabase:
    """
    Return the MongoDB database instance.

    Returns:
        AsyncIOMotorDatabase
    """

    return get_database()