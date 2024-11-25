import uuid

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from pytest_fastapi_deps import FixtureDependencyOverrider
from starlette import status

from app.domains.models.user_model import UserModel
from app.repositories.user_repository import UserRepository
from app.middlewares.auth.deps import get_current_user


@pytest.mark.anyio
async def test_creation(
    fastapi_app: FastAPI,
    client: AsyncClient,
    fastapi_dep: type[FixtureDependencyOverrider],
) -> None:
    """Tests user instance creation."""
    with fastapi_dep(fastapi_app).override(
        {
            get_current_user: UserModel(
                id=1,
                full_name="test",
                email="test@example.com",
                hashed_password=uuid.uuid4().hex,
                is_superuser=True,
            ),  # type: ignore
        },
    ):
        url = fastapi_app.url_path_for("create_user")
        test_name = uuid.uuid4().hex
        response = await client.post(
            url,
            json={
                "full_name": test_name,
                "email": f"{test_name}@example.com",
                "password": test_name,
                "is_superuser": True,
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        instances = await UserRepository.get_user_by_email(
            email=f"{test_name}@example.com",
        )
        assert instances.full_name == test_name


@pytest.mark.anyio
async def test_getting(
    fastapi_app: FastAPI,
    client: AsyncClient,
    fastapi_dep: type[FixtureDependencyOverrider],
) -> None:
    """Tests user instance retrieval."""
    with fastapi_dep(fastapi_app).override(
        {
            get_current_user: UserModel(
                id=1,
                full_name="test",
                email="test@example.com",
                hashed_password=uuid.uuid4().hex,
                is_superuser=True,
            ),  # type: ignore
        },
    ):
        test_name = uuid.uuid4().hex
        await UserRepository.create_user(
            full_name=test_name,
            email=f"{test_name}@example.com",
            password=test_name,
            is_superuser=True,
        )
        url = fastapi_app.url_path_for("list_users")
        response = await client.get(url)
        users = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert len(users) == 1
        assert users[0]["full_name"] == test_name
