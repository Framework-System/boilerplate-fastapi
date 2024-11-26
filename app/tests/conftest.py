from typing import Any, AsyncGenerator, Dict

import nest_asyncio
import pytest
from fastapi import FastAPI
from fastapi import status as http_status
from httpx import AsyncClient
from tortoise import Tortoise
from tortoise.contrib.test import finalizer, initializer

from app.api.application import get_app
from app.domains.database import MODELS_MODULES, TORTOISE_CONFIG
from app.settings import settings

nest_asyncio.apply()


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """
    Backend for anyio pytest plugin.

    :return: backend name.
    """
    return "asyncio"


@pytest.fixture(autouse=True)
async def initialize_db() -> AsyncGenerator[None, None]:
    """
    Initialize models and database.

    :yields: Nothing.
    """
    initializer(
        MODELS_MODULES,
        db_url=str(settings.db_url),
        app_label="models",
    )
    await Tortoise.init(config=TORTOISE_CONFIG)

    yield

    await Tortoise.close_connections()
    finalizer()


@pytest.fixture
def fastapi_app() -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    return get_app()


@pytest.fixture
async def client(
    fastapi_app: FastAPI,
    anyio_backend: Any,
) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: the application.
    :yield: client for the app.
    """
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def authenticated_client(
    client: AsyncClient,
    fastapi_app: FastAPI,
    user_data: dict[str, Any],
) -> AsyncClient:
    """
    Fixture for creating a client authenticated with a user.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    :param user_data: user data to create and authenticate.
    :return: authenticated client.
    """
    # Create a user
    url = fastapi_app.url_path_for("create_user")
    response = await client.post(url=url, json=user_data)
    assert response.status_code == http_status.HTTP_201_CREATED

    # Authenticate
    url = fastapi_app.url_path_for("access_token")
    data = {
        "username": user_data.get("email"),
        "password": user_data.get("password"),
    }
    response = await client.post(url=url, data=data)
    assert response.status_code == http_status.HTTP_200_OK
    token = response.json()["access_token"]

    # Update client with authentication headers
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


@pytest.fixture
async def superuser_client(
    client: AsyncClient,
    fastapi_app: FastAPI,
    user_data: dict[str, Any],
) -> AsyncClient:
    """
    Fixture for creating a client authenticated with a superuser.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    :param user_data: user data to create and authenticate.
    :return: superuser client.
    """
    user_data["is_superuser"] = True

    # Create a user
    url = fastapi_app.url_path_for("create_user")
    response = await client.post(url=url, json=user_data)
    assert response.status_code == http_status.HTTP_201_CREATED

    # Authenticate
    url = fastapi_app.url_path_for("access_token")
    data = {
        "username": user_data.get("email"),
        "password": user_data.get("password"),
    }
    response = await client.post(url=url, data=data)
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Update client with authentication headers
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


@pytest.fixture
def user_data() -> Dict[str, Any]:
    """
    Fixture for creating a user data.

    :return: user data.
    """
    return {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "securepassword",
        "is_superuser": False,
    }
