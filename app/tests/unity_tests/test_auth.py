from typing import Any

import pytest
from fastapi import FastAPI
from fastapi import status as http_status
from httpx import AsyncClient


@pytest.mark.anyio
async def test_authentication_with_incorrect_username(
    client: AsyncClient,
    fastapi_app: FastAPI,
    user_data: dict[str, Any],
) -> None:
    """Test authenticating with incorrect username."""
    # Create a user
    url = fastapi_app.url_path_for("create_user")
    response = await client.post(url=url, json=user_data)
    assert response.status_code == http_status.HTTP_201_CREATED

    url = fastapi_app.url_path_for("access_token")
    data = {
        "username": "test",
        "password": "test",
    }
    response = await client.post(url=url, data=data)

    assert response.status_code == http_status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_authentication_with_incorrect_password(
    client: AsyncClient,
    fastapi_app: FastAPI,
    user_data: dict[str, Any],
) -> None:
    """Test authentication with incorrect password."""
    # Create a user
    url = fastapi_app.url_path_for("create_user")
    response = await client.post(url=url, json=user_data)
    assert response.status_code == http_status.HTTP_201_CREATED

    url = fastapi_app.url_path_for("access_token")
    data = {
        "username": user_data.get("email"),
        "password": "test",
    }
    response = await client.post(url=url, data=data)

    assert response.status_code == http_status.HTTP_400_BAD_REQUEST
