from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from pymongo import AsyncMongoClient


MONGODB_URL = "mongodb://localhost:27017/"
DATABASE_NAME = "mongodb_task"


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncMongoClient(MONGODB_URL)

    app.state.mongodb_client = client
    app.state.database = client[DATABASE_NAME]

    try:
        await client.admin.command("ping")
        print("Connected to MongoDB successfully!")

        yield
    finally:
        await client.close()


def get_database(request: Request):
    return request.app.state.database