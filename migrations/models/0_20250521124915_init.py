from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "recipient" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "full_name" VARCHAR(150) NOT NULL UNIQUE,
    "address" VARCHAR(250) NOT NULL UNIQUE,
    "phone_number_1" VARCHAR(15) NOT NULL UNIQUE,
    "phone_number_2" VARCHAR(15) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "users" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "first_name" VARCHAR(50),
    "last_name" VARCHAR(50),
    "email" VARCHAR(200) NOT NULL UNIQUE,
    "password" VARCHAR(200) NOT NULL,
    "is_verified" INT NOT NULL DEFAULT 0,
    "is_superuser" INT NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS "dispatch" (
    "id" CHAR(36) NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "status" VARCHAR(10) NOT NULL DEFAULT 'PENDING' /* PENDING: PENDING\nPICKED: PROCESSING\nACCESSING: ACCESSING\nPACKAGING: PACKAGING\nEN_ROUTE: EN ROUTE\nDELIVERED: DELIVERED */,
    "content" TEXT NOT NULL,
    "weight" INT NOT NULL,
    "note" TEXT NOT NULL,
    "delievery_date" DATE NOT NULL,
    "code" VARCHAR(16) NOT NULL UNIQUE,
    "recipient_id" CHAR(36) REFERENCES "recipient" ("id") ON DELETE SET NULL,
    "sender_id" CHAR(36) NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
