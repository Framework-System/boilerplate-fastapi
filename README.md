# Boilerplate FastAPI

An example of an API focused on microservices, using best practices.

## Poetry

This project uses poetry. It's a modern dependency management
tool.

To run the project use this set of commands:

```bash
poetry install
poetry run python -m app
```

This will start the server on the configured host.

You can find swagger documentation at `/api/docs`.

You can read more about poetry here: <https://python-poetry.org/>

## Docker

You can start the project with docker using this command:

```bash
docker-compose -f dockerfiles/docker-compose.yml --project-directory . up --build
```

If you want to develop in docker with autoreload add `-f dockerfiles/docker-compose.dev.yml` to your docker command.
Like this:

```bash
docker-compose -f dockerfiles/docker-compose.yml -f dockerfiles/docker-compose.dev.yml --project-directory . up --build
```

This command exposes the web application on port 8000, mounts current directory and enables autoreload.

But you have to rebuild image every time you modify `poetry.lock` or `pyproject.toml` with this command:

```bash
docker-compose -f dockerfiles/docker-compose.yml --project-directory . build
```

## Project structure

```bash
$ tree "app"
app
└── api  # Package contains web server. Handlers, startup config.
    ├── routes  # Package with all handlers.
        └── router.py  # Main router.
    ├── application.py  # FastAPI application configuration.
    └── lifetime.py  # Contains actions to perform on startup and shutdown.
├── clients  # Package for different external client services such as Aws S3 or redis etc.
├── domains  # Package contains different domain classes.
    ├── models  # Package contains different models for ORMs.
    └── repositories  # Package contains different classes to interact with database.
├── middlewares  # Package contains different middlewares.
    └── auth  # Package contains authentication middlewares.
├── services  # Package contains the business logical classes.
├── tests  # Package contains Tests for project.
├── __main__.py  # Startup script. Starts uvicorn.
├── conftest.py  # Fixtures for all tests.
├── logging  # Logger configurations.
├── settings.py  # Main configuration settings for project.
```

## Configuration

This application can be configured with environment variables.

You can create `.env` file in the root directory and place all
environment variables here.

All environment variables should start with "APP" prefix.

For example if you see in your "app/settings.py" a variable named like
`random_parameter`, you should provide the "APP_RANDOM_PARAMETER"
variable to configure the value. This behaviour can be changed by overriding `env_prefix` property
in `app.settings.Settings.Config`.

An example of .env file:

```bash
APP_RELOAD="True"
APP_PORT="8000"
APP_ENVIRONMENT="dev"
```

You can read more about BaseSettings class here: <https://pydantic-docs.helpmanual.io/usage/settings/>

## Pre-commit

To install pre-commit simply run inside the shell:

```bash
pre-commit install
```

pre-commit is very useful to check your code before publishing it.
It's configured using .pre-commit-config.yaml file.

By default it runs:

* black (formats your code);
* mypy (validates types);
* isort (sorts imports in all files);
* flake8 (spots possible bugs);

You can read more about pre-commit here: <https://pre-commit.com/>

## Migration generation

To generate migrations you should run:

```bash
docker-compose -f dockerfiles/docker-compose.yml -f dockerfiles/docker-compose.dev.yml --project-directory . run api aerich migrate
```

## Apply migrations

If you want to apply migrations, you should run:

```bash
# Upgrade database to the last migration.
docker-compose -f dockerfiles/docker-compose.yml -f dockerfiles/docker-compose.dev.yml --project-directory . run api aerich upgrade
```

### Reverting migrations

If you want to revert migrations, you should run:

```bash
docker-compose -f dockerfiles/docker-compose.yml -f dockerfiles/docker-compose.dev.yml --project-directory . run api aerich downgrade
```

## Running tests

If you want to run it in docker, simply run:

```bash
docker-compose -f dockerfiles/docker-compose.yml -f dockerfiles/docker-compose.dev.yml --project-directory . run --build --rm api pytest -vv .
```
