from typing import Any, List

from fastapi import APIRouter, HTTPException
from fastapi import status as http_status
from fastapi.param_functions import Depends

from app.api.routes.v1.users.dtos import UserCreateInputDTO, UserDTO, UserUpdateInputDTO
from app.domains.models.user_model import UserModel
from app.middlewares.auth.deps import CurrentUser
from app.services.user_service import UserService

# Define the API router for user models.
router = APIRouter()


@router.post("/", response_model=UserDTO, status_code=201)
async def create_user(
    dto: UserCreateInputDTO,
    service: UserService = Depends(),
) -> UserModel:
    """
    Creates user object in the database.

    :param dto: new user model object.
    :param service: Service for user models.
    :return: created user object.
    """
    return await service.create_user(
        email=dto.email,
        full_name=dto.full_name,
        password=dto.password,
        is_superuser=dto.is_superuser,
    )


@router.get("/", response_model=List[UserDTO])
async def list_users(
    current_user: CurrentUser,
    limit: int = 100,
    offset: int = 0,
    service: UserService = Depends(),
) -> List[UserModel]:
    """
    List all user objects from the database.

    :param current_user: The current user object.
    :param limit: limit of user objects, defaults to 100.
    :param offset: offset of user objects, defaults to 0.
    :param service: Service for user models.
    :return: list of user objects from database.
    """
    return await service.list_users(limit=limit, offset=offset)


@router.put("/{user_id}", response_model=UserDTO, status_code=200)
async def update_user(
    current_user: CurrentUser,
    user_id: str,
    dto: UserUpdateInputDTO,
    service: UserService = Depends(),
) -> UserModel:
    """
    Update user object in the database.

    :param current_user : The current user object.
    :param user_id: user id.
    :param dto: user model object.
    :param service: Service for user models.
    :return: updated user object.
    """
    return await service.update_user(
        user_id=user_id,
        email=dto.email,
        full_name=dto.full_name,
        is_superuser=dto.is_superuser,
    )


@router.get("/me", response_model=UserDTO)
async def get_me(current_user: CurrentUser) -> Any:
    """
    Retrieve user object from the current user.

    :param current_user : The current user object.
    :return: User object from current user.
    """
    return await current_user


@router.get("/email-list", response_model=List[str])
async def list_users_emails(
    current_user: CurrentUser,
    limit: int = 100,
    offset: int = 0,
    service: UserService = Depends(),
) -> List[str]:
    """
    List emails of the users from the database.

    :param current_user: The current user object.
    :param limit: limit of user objects, defaults to 100.
    :param offset: offset of user objects, defaults to 0.
    :param service: Service for user models.
    :return: list of users emails.
    :raises HTTPException: If the user doesn't have enough privileges.
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="Not enough privileges",
        )

    return await service.list_users_emails(
        limit=limit,
        offset=offset,
    )
