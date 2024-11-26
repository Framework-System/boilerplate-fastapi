from typing import List

from app.domains.models.user_model import UserModel
from app.repositories.user_repository import UserRepository


class UserService:
    """Class for user operations."""

    def __init__(self) -> None:
        self.repository = UserRepository

    async def create_user(
        self,
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
        return await self.repository.create_user(
            email=email,
            full_name=full_name,
            password=password,
            is_superuser=is_superuser,
        )

    async def update_user(
        self,
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
        return await self.repository.update_user(
            user_id=user_id,
            email=email,
            full_name=full_name,
            is_superuser=is_superuser,
        )

    async def get_user_by_email(self, email: str) -> UserModel:
        """
        Get user by email.

        :param email: email of users.
        :return: user object.
        """
        return await self.repository.get_user_by_email(email=email)

    async def get_user_by_id(self, user_id: str) -> UserModel:
        """
        Get user by id.

        :param user_id: id of users.
        :return: user.
        """
        return await self.repository.get_user_by_id(user_id)

    async def list_users(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> List[UserModel]:
        """
        Get all user models with limit/offset pagination.

        :param limit: limit of users.
        :param offset: offset of users.
        :return: stream of users.
        """
        return await self.repository.list_users(limit, offset)

    async def list_users_emails(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> List[str]:
        """
        List emails of the users from the database.

        :param limit: limit of users.
        :param offset: offset of users.
        :return: users emails.
        """
        users = await self.repository.list_users(limit, offset)
        return [user.email for user in users]
