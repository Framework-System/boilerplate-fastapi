from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from app.api.lifetime import register_shutdown_event, register_startup_event
from app.api.routes.router import api_router
from app.domains.database import TORTOISE_CONFIG
from app.logging import configure_logging
from app.settings import settings


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    if settings.environment == "dev":
        import ptvsd  # noqa: WPS433

        ptvsd.enable_attach(address=("0.0.0.0", 5678))  # noqa: S104

    configure_logging()

    app = FastAPI(
        title=settings.app_name,
        version=metadata.version(settings.root_path),
        docs_url=f"{settings.api_prefix}/docs",
        redoc_url=f"{settings.api_prefix}/redoc",
        openapi_url=f"{settings.api_prefix}/openapi.json",
        default_response_class=ORJSONResponse,
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix=settings.api_prefix)

    # Configures tortoise orm.
    register_tortoise(
        app,
        config=TORTOISE_CONFIG,
        add_exception_handlers=True,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.backend_cors_origins
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
