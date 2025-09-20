from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "feedback" (
    "created" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "modified" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "id" VARCHAR(20) NOT NULL PRIMARY KEY,
    "username" VARCHAR(50) NOT NULL,
    "product_article" INT NOT NULL,
    "valuation" INT NOT NULL,
    "comment" TEXT,
    "pros" TEXT,
    "cons" TEXT,
    "created_on_wb" TIMESTAMPTZ NOT NULL
);
COMMENT ON TABLE "feedback" IS 'Represent Feedback db model.';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
