"""
Auth Routes

API endpoints for user registration and authentication.
"""

from __future__ import annotations

from fastapi import APIRouter, status

from app.controllers.auth_controller import auth_controller
from app.schemas.auth_schema import (
    TokenResponseSchema,
    UserLoginSchema,
    UserRegisterSchema,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=TokenResponseSchema,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new account",
    description="Create a new user account with full name, email, and matching password.",
)
async def register_account(
    schema: UserRegisterSchema,
) -> TokenResponseSchema:
    """
    Register a new user account.
    """

    return await auth_controller.register(schema)


@router.post(
    "/login",
    response_model=TokenResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Login to account",
    description="Authenticate with email and password to receive a JWT access token.",
)
async def login_account(
    schema: UserLoginSchema,
) -> TokenResponseSchema:
    """
    Authenticate an existing user.
    """

    return await auth_controller.login(schema)
