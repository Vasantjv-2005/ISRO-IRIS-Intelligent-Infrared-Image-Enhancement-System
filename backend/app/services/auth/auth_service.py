"""
Auth Service

Business logic for user registration, authentication, password hashing,
and JWT token generation. Follows Clean Architecture principles.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
import jwt

from app.core.settings import settings
from app.middleware.error_handler import (
    ConflictException,
    UnauthorizedException,
)
from app.models.user_model import UserModel
from app.repositories.user_repository import user_repository
from app.schemas.auth_schema import (
    TokenResponseSchema,
    UserLoginSchema,
    UserRegisterSchema,
    UserResponseSchema,
)
from app.utils.logger import Logger

logger = Logger.get_logger(__name__)


class AuthService:
    """
    Service handling user authentication and token management.
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a plaintext password using bcrypt.
        """

        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    @staticmethod
    def verify_password(plaintext: str, hashed: str) -> bool:
        """
        Verify a plaintext password against a stored hash.
        """

        try:
            return bcrypt.checkpw(
                plaintext.encode("utf-8"),
                hashed.encode("utf-8"),
            )
        except Exception:
            return False

    @staticmethod
    def create_access_token(
        data: dict,
        expires_delta: Optional[timedelta] = None,
    ) -> str:
        """
        Generate a JWT access token.
        """

        to_encode = data.copy()

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )

        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )

        return encoded_jwt

    async def register_user(
        self,
        schema: UserRegisterSchema,
    ) -> TokenResponseSchema:
        """
        Register a new user account.
        """

        logger.info("Starting registration for email: %s", schema.email)

        existing_user = await user_repository.get_by_email(schema.email)

        if existing_user:
            logger.warning(
                "Registration failed - email already exists: %s",
                schema.email,
            )
            raise ConflictException(
                "An account with this email address already exists."
            )

        hashed_pw = self.hash_password(schema.password)

        new_user = UserModel(
            full_name=schema.full_name.strip(),
            email=schema.email.lower().strip(),
            hashed_password=hashed_pw,
        )

        created_user = await user_repository.create(new_user)

        logger.info(
            "User registered successfully: %s (ID: %s)",
            created_user.email,
            created_user.user_id,
        )

        token_payload = {
            "sub": created_user.user_id,
            "email": created_user.email,
        }
        access_token = self.create_access_token(token_payload)

        user_response = UserResponseSchema(
            user_id=created_user.user_id,
            full_name=created_user.full_name,
            email=created_user.email,
            is_active=created_user.is_active,
            created_at=created_user.created_at,
        )

        return TokenResponseSchema(
            access_token=access_token,
            token_type="bearer",
            user=user_response,
            message="Account created successfully.",
        )

    async def login_user(
        self,
        schema: UserLoginSchema,
    ) -> TokenResponseSchema:
        """
        Authenticate an existing user and return a JWT token.
        """

        logger.info("Attempting login for email: %s", schema.email)

        user = await user_repository.get_by_email(schema.email)

        if not user or not self.verify_password(schema.password, user.hashed_password):
            logger.warning("Login failed for email: %s", schema.email)
            raise UnauthorizedException("Invalid email or password.")

        if not user.is_active:
            logger.warning("Login attempted for deactivated user: %s", schema.email)
            raise UnauthorizedException("This account has been deactivated.")

        logger.info("User logged in successfully: %s", user.email)

        token_payload = {
            "sub": user.user_id,
            "email": user.email,
        }
        access_token = self.create_access_token(token_payload)

        user_response = UserResponseSchema(
            user_id=user.user_id,
            full_name=user.full_name,
            email=user.email,
            is_active=user.is_active,
            created_at=user.created_at,
        )

        return TokenResponseSchema(
            access_token=access_token,
            token_type="bearer",
            user=user_response,
            message="Login successful.",
        )


auth_service = AuthService()
