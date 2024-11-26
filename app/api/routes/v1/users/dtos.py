import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class UserDTO(BaseModel):
    """
    DTO for user models.

    It returned when accessing user models from the API.
    """

    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    email: str
    full_name: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserCreateInputDTO(BaseModel):
    """DTO for creating new user model."""

    email: str
    full_name: str
    password: str
    is_superuser: bool


class UserUpdateInputDTO(BaseModel):
    """DTO for updating existing user model."""

    full_name: str
    email: str
    is_superuser: bool
