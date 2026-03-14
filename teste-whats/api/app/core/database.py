from contextlib import asynccontextmanager

from fastapi import FastAPI
from pymongo import ASCENDING, AsyncMongoClient
from pymongo.server_api import ServerApi

from app.core.config import get_settings

client: AsyncMongoClient | None = None
database = None


async def connect_to_mongo() -> None:
    global client, database

    settings = get_settings()
    client = AsyncMongoClient(
        settings.mongodb_uri,
        server_api=ServerApi("1"),
        appname=settings.app_name,
    )
    database = client[settings.mongodb_db_name]
    await database.command("ping")
    await database["whatsapp_sessions"].create_index(
        [("session_key", ASCENDING)],
        unique=True,
        name="uq_whatsapp_sessions_session_key",
    )


async def close_mongo_connection() -> None:
    global client, database

    if client is not None:
        client.close()
        client = None
        database = None


def get_database():
    if database is None:
        raise RuntimeError("MongoDB connection has not been initialized.")
    return database


@asynccontextmanager
async def lifespan(_: FastAPI):
    await connect_to_mongo()
    try:
        yield
    finally:
        await close_mongo_connection()
