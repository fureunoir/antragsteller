from asyncio import sleep
from contextlib import asynccontextmanager
from os import getenv

import sentry_sdk
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from sentry_sdk import capture_exception
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.responses import RedirectResponse

from src.bot import bot
from src.handlers import router
from src.logging import logger

sentry_sdk.init(
    dsn=getenv("SENTRY_DSN"),
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

@asynccontextmanager
async def lifespan(_app: FastAPI):
    client = AsyncIOMotorClient(getenv("MONGO_URI", "mongodb://db:27017"))

    yield

    client.close()

app = FastAPI(lifespan=lifespan,
              title="Antragsteller API",
              description="This API powers the all-in-one Telegram bot for chat moderation, notifications, and more.",
              version="0.1.0",
              docs_url="/docs/swagger",
              redoc_url="/docs/redoc")

app.add_middleware(SentryAsgiMiddleware)  # type: ignore

app.include_router(router)

@app.get("/")
def index():
    return RedirectResponse(url="https://t.me/fureunoir")
