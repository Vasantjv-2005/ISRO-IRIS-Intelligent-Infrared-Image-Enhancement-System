"""
User Repository

Handles all database operations related to user accounts.
"""

from __future__ import annotations

from typing import Optional

from motor.motor_asyncio import AsyncIOMotorCollection

from app.database.mongodb import get_database
from app.models.user_model import UserModel
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


class UserRepository:
    """
    Repository responsible for Users collection in MongoDB.
    """

    COLLECTION = "users"

    @property
    def collection(self) -> AsyncIOMotorCollection:
        """
        Return MongoDB users collection.
        """

        db = get_database()

        return db[self.COLLECTION]

    # =====================================================
    # Create
    # =====================================================

    async def create(
        self,
        user: UserModel,
    ) -> UserModel:
        """
        Insert a new user document into the collection.
        """

        document = user.model_dump(by_alias=True)

        logger.debug("Inserting new user document for email: %s", user.email)

        await self.collection.insert_one(document)

        return user

    # =====================================================
    # Read
    # =====================================================

    async def get_by_email(
        self,
        email: str,
    ) -> Optional[UserModel]:
        """
        Retrieve a user document by their email address.
        """

        logger.debug("Querying user by email: %s", email)

        document = await self.collection.find_one(
            {"email": email.lower().strip()},
        )

        if not document:
            return None

        return UserModel.model_validate(document)

    async def get_by_id(
        self,
        user_id: str,
    ) -> Optional[UserModel]:
        """
        Retrieve a user document by user_id.
        """

        logger.debug("Querying user by id: %s", user_id)

        document = await self.collection.find_one(
            {"user_id": user_id},
        )

        if not document:
            return None

        return UserModel.model_validate(document)


user_repository = UserRepository()
