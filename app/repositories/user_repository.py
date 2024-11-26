from typing import List

from app.domains.models.user_model import UserModel
from app.middlewares.auth.security import get_password_hash


class UserRepository:
    """Class for accessing user table."""

    @classmethod
    async def create_user(
        cls,
        full_name: str,
        email: str,
        password: str,
        is_superuser: bool,
    ) -> UserModel:
        """
        Add single user to session.

        :param full_name: full_name of a user.
        :param email: email of a user.
        :param password: password of a user.
        :param is_superuser: is_superuser of a user.
        :return: user object.
        """
        return await UserModel.create(
            full_name=full_name,
            email=email,
            hashed_password=get_password_hash(password),
            is_superuser=is_superuser,
        )

    @classmethod
    async def update_user(
        cls,
        user_id: str,
        full_name: str,
        email: str,
        is_superuser: bool,
    ) -> UserModel:
        """
        Update single user to session.

        :param user_id: id of a user.
        :param full_name: full_name of a user.
        :param email: email of a user.
        :param is_superuser: is_superuser of a user.
        :return: user object.
        """
        user = await UserModel.get(id=user_id)
        user.full_name = full_name
        user.email = email
        user.is_superuser = is_superuser
        await user.save()
        return user

    @classmethod
    async def get_user_by_id(cls, user_id: str) -> UserModel:
        """
        Get user by id.

        :param user_id: id of users.
        :return: user object.
        """
        return await UserModel.get(id=user_id)

    @classmethod
    async def get_user_by_email(cls, email: str) -> UserModel:
        """
        Get user by email.

        :param email: email of users.
        :return: user object.
        """
        return await UserModel.get(email=email)

    @classmethod
    async def list_users(
        cls,
        limit: int = 100,
        offset: int = 0,
    ) -> List[UserModel]:
        """
        List all user with limit/offset pagination.

        :param limit: limit of users.
        :param offset: offset of users.
        :return: list of users.
        """
        return await UserModel.all().offset(offset).limit(limit)
