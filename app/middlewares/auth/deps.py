from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from pydantic import ValidationError

from app.domains.models.user_model import UserModel
from app.repositories.user_repository import UserRepository
from app.middlewares.auth.security import TokenDep, TokenPayload, verify_password
from app.settings import settings


async def get_current_user(token: TokenDep) -> UserModel:
    """
    Asynchronously retrieves the current user from the provided JWT token.

    :param token: The JWT token containing the user's authentication information.
    :return: User.
    :raises HTTPException: If the user is not found or inactive.
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    user = (
        await UserRepository.get_user_by_id(token_data.sub) if token_data.sub else None
    )
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:  # type: ignore
        raise HTTPException(status_code=400, detail="Inactive user")
    return user  # type: ignore


CurrentUser = Annotated[UserModel, Depends(get_current_user)]


def get_current_active_superuser(current_user: CurrentUser) -> UserModel:
    """
    Check if the current user has superuser privileges and raise an HTTPException if not.

    :param current_user : The current user object.
    :return: User.
    :raises HTTPException: If the user doesn't have enough privileges.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400,
            detail="The user doesn't have enough privileges",
        )
    return current_user


async def authenticate(email: str, password: str) -> UserModel | None:
    """
    Authenticates a user by checking if the provided email and password match.

    :param email: The email of the user.
    :param password: The password of the user.
    :return: User.
    """
    db_user = await UserRepository.get_user_by_email(email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):  # type: ignore
        return None
    return db_user  # type: ignore
