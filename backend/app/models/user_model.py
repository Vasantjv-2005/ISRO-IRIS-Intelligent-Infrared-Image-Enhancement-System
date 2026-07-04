"""
User Model

Defines the structure of a user document stored in MongoDB.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, EmailStr, Field


def utc_now() -> datetime:
    """
    Return the current UTC datetime.
    """

    return datetime.now(timezone.utc)


class UserModel(BaseModel):
    """
    User document stored in MongoDB.
    """

    user_id: str = Field(default_factory=lambda: str(uuid4()))

    full_name: str

    email: str

    hashed_password: str

    is_active: bool = True

    created_at: datetime = Field(default_factory=utc_now)

    updated_at: datetime = Field(default_factory=utc_now)

    model_config = {
        "populate_by_name": True,
        "extra": "ignore",
        "validate_assignment": True,
    }
