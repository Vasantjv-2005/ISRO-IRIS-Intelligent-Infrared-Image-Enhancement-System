"""
Auth Schemas

Request and response schemas for user registration and authentication.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr, Field, model_validator


class UserRegisterSchema(BaseModel):
    """
    Schema for creating a new user account.
    """

    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Full name of the user.",
    )

    email: EmailStr = Field(
        ...,
        description="Unique email address for login.",
    )

    password: str = Field(
        ...,
        min_length=6,
        description="Account password (at least 6 characters).",
    )

    confirm_password: str = Field(
        ...,
        description="Must match the password field precisely.",
    )

    @model_validator(mode="after")
    def verify_passwords_match(self) -> UserRegisterSchema:
        """
        Ensure password and confirm_password match.
        """

        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match.")

        return self


class UserLoginSchema(BaseModel):
    """
    Schema for user login.
    """

    email: str = Field(
        ...,
        description="Registered email address.",
    )

    password: str = Field(
        ...,
        description="Account password.",
    )


class UserResponseSchema(BaseModel):
    """
    Schema for user profile responses.
    """

    user_id: str

    full_name: str

    email: str

    is_active: bool

    created_at: datetime


class TokenResponseSchema(BaseModel):
    """
    Schema returned after successful authentication or login.
    """

    access_token: str

    token_type: str = "bearer"

    user: UserResponseSchema

    message: str = "Authentication successful."
