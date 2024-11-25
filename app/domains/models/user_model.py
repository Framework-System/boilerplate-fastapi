from tortoise import fields, models

from app.domains.models.base_model import BaseModel


class UserModel(models.Model, BaseModel):
    """Model for auth user."""

    email = fields.CharField(max_length=200, unique=True, index=True)
    full_name = fields.CharField(max_length=200)
    hashed_password = fields.CharField(max_length=200)
    is_superuser = fields.BooleanField(default=False)

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        table = "users"
