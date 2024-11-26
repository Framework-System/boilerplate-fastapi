from typing import Any

import pytest
from fastapi import FastAPI
from fastapi import status as http_status
from httpx import AsyncClient

from app.api.routes.v1.users.dtos import UserDTO


@pytest.mark.anyio
async def test_create_user(
    client: AsyncClient,
    fastapi_app: FastAPI,
    user_data: dict[str, Any],
) -> None:
    """Test create user endpoint."""
    url = fastapi_app.url_path_for("create_user")
    response = await client.post(url=url, json=user_data)

    assert response.status_code == http_status.HTTP_201_CREATED

    response_data = response.json()
    validated_user = UserDTO(**response_data)

    assert validated_user.email == user_data.get("email")
    assert validated_user.full_name == user_data.get("full_name")
    assert validated_user.is_superuser == user_data.get("is_superuser")


@pytest.mark.anyio
async def test_list_users(
    authenticated_client: AsyncClient,
    fastapi_app: FastAPI,
    user_data: dict[str, Any],
) -> None:
    """Test list users endpoint."""
    url = fastapi_app.url_path_for("list_users")
    response = await authenticated_client.get(url=url)

    assert response.status_code == http_status.HTTP_200_OK

    response_data = response.json()

    assert isinstance(response_data, list)

    for user in response_data:
        validated_user = UserDTO(**user)

        assert validated_user.email == user_data.get("email")
        assert validated_user.full_name == user_data.get("full_name")
        assert validated_user.is_superuser == user_data.get("is_superuser")


@pytest.mark.anyio
async def test_get_me(
    authenticated_client: AsyncClient,
    fastapi_app: FastAPI,
    user_data: dict[str, Any],
) -> None:
    """Test get me endpoint."""
    url = fastapi_app.url_path_for("get_me")
    response = await authenticated_client.get(url=url)

    assert response.status_code == http_status.HTTP_200_OK

    response_data = response.json()
    validated_user = UserDTO(**response_data)

    assert validated_user.email == user_data.get("email")
    assert validated_user.full_name == user_data.get("full_name")
    assert validated_user.is_superuser == user_data.get("is_superuser")


@pytest.mark.anyio
async def test_get_me_without_authentication(
    client: AsyncClient,
    fastapi_app: FastAPI,
) -> None:
    """Test get me endpoint without authentication."""
    url = fastapi_app.url_path_for("get_me")
    response = await client.get(url=url)
    assert response.status_code == http_status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_update_user(
    authenticated_client: AsyncClient,
    fastapi_app: FastAPI,
    user_data: dict[str, Any],
) -> None:
    """Test update user endpoint."""
    # Assuming the current user is set in the test environment
    get_me_url = fastapi_app.url_path_for("get_me")
    get_me_response = await authenticated_client.get(url=get_me_url)

    assert get_me_response.status_code == http_status.HTTP_200_OK

    get_me_response_data = get_me_response.json()
    user_id = get_me_response_data.get("id")

    updated_data = user_data.copy()
    updated_data["full_name"] = "Updated User"

    url = fastapi_app.url_path_for("update_user", user_id=user_id)
    response = await authenticated_client.put(url=url, json=updated_data)

    assert response.status_code == http_status.HTTP_200_OK

    response_data = response.json()
    validated_user = UserDTO(**response_data)

    assert str(validated_user.id) == user_id
    assert validated_user.full_name == updated_data.get("full_name")


@pytest.mark.anyio
async def test_list_users_emails(
    superuser_client: AsyncClient,
    fastapi_app: FastAPI,
) -> None:
    """Test list users emails endpoint."""
    url = fastapi_app.url_path_for("list_users_emails")
    response = await superuser_client.get(url=url)

    assert response.status_code == http_status.HTTP_200_OK
    assert isinstance(response.json(), list)


@pytest.mark.anyio
async def test_list_users_emails_without_superuser(
    authenticated_client: AsyncClient,
    fastapi_app: FastAPI,
) -> None:
    """Test list users emails without superuser."""
    url = fastapi_app.url_path_for("list_users_emails")
    response = await authenticated_client.get(url=url)

    assert response.status_code == http_status.HTTP_403_FORBIDDEN
