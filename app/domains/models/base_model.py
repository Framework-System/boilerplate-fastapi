import uuid

from tortoise import fields


class BaseModel:
    """Base model for all database models."""

    id = fields.UUIDField(pk=True, default_factory=uuid.uuid4)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
