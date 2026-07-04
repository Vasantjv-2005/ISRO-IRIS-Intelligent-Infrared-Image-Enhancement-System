"""
Auth Controller

Handles authentication requests by delegating business logic
to the Auth Service.
"""

from __future__ import annotations

from app.schemas.auth_schema import (
    TokenResponseSchema,
    UserLoginSchema,
    UserRegisterSchema,
)
from app.services.auth.auth_service import auth_service


class AuthController:
    """
    Controller responsible for user authentication operations.
    """

    async def register(
        self,
        schema: UserRegisterSchema,
    ) -> TokenResponseSchema:
        """
        Register a new user account.
        """

        return await auth_service.register_user(schema)

    async def login(
        self,
        schema: UserLoginSchema,
    ) -> TokenResponseSchema:
        """
        Authenticate a user and generate an access token.
        """

        return await auth_service.login_user(schema)


auth_controller = AuthController()
