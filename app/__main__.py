import uvicorn

from app.settings import settings


def main() -> None:
    """Entrypoint of the application."""
    uvicorn.run(
        "app.api.application:get_app",
        workers=settings.workers_count,
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.value.lower(),
        factory=True,
        timeout_keep_alive=600,
    )


if __name__ == "__main__":
    main()
