"""
Database Dependency

This module provides a reusable MongoDB database instance
for FastAPI routes and services.
"""

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database.mongodb import mongodb


def get_database() -> AsyncIOMotorDatabase:
    """
    Returns the active MongoDB database instance.

    Usage:
        db = get_database()
    """

    if mongodb.database is None:
        raise RuntimeError(
            "MongoDB is not connected. Please check your database connection."
        )

    return mongodb.database