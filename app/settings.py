import enum
from pathlib import Path
from tempfile import gettempdir

from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

TEMP_DIR = Path(gettempdir())


class LogLevel(enum.StrEnum):
    """Possible log levels."""

    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    FATAL = "FATAL"


class Settings(BaseSettings):
    """
    Application settings.

    These parameters can be configured
    with environment variables.
    """

    app_name: str = "Boilerplate FastAPI"
    root_path: str = Path(__file__).parent.name

    host: str = "127.0.0.1"
    port: int = 8000

    # Quantity of workers for uvicorn
    workers_count: int = 1

    # Enable uvicorn reloading
    reload: bool = False

    # Current environment
    environment: str = "dev"

    # Variables for security
    secret_key: str = "dev"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 8

    api_prefix: str = "/api"
    backend_cors_origins: list[str] = ["*"]

    log_level: LogLevel = LogLevel.INFO

    # Variables for the database
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "app"
    db_pass: str = "app"
    db_base: str = "app"
    db_echo: bool = False

    # Variables for AWS S3
    default_bucket: str = "frwk-ai-boilerplate-fastapi"

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgres",
            host=self.db_host,
            port=self.db_port,
            user=self.db_user,
            password=self.db_pass,
            path=f"/{self.db_base}",
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        env_file_encoding="utf-8",
        extra="allow",
    )


settings = Settings()
