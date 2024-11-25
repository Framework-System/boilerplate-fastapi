from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
    CREATE TABLE IF NOT EXISTS "users" (
        "id" UUID NOT NULL  PRIMARY KEY,
        "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
        "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
        "full_name" VARCHAR(200) NOT NULL,
        "email" VARCHAR(200) NOT NULL UNIQUE,
        "hashed_password" VARCHAR(200) NOT NULL,
        "is_active" BOOL NOT NULL  DEFAULT True,
        "is_superuser" BOOL NOT NULL  DEFAULT False
    );
    CREATE INDEX IF NOT EXISTS "idx_users_email_1b4f1c" ON "users" ("email");
    COMMENT ON TABLE "users" IS 'Model for auth user.';
    """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
    DROP TABLE IF EXISTS "users";
    """
