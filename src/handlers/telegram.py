from asyncio import create_task
from os import getenv

from aiogram.types import Update

from src.handlers import router
from src.helpers.bot import handle_message

url_part = getenv("TELEGRAM_BOT_TOKEN")

@router.post(f"/webhook/{url_part}", include_in_schema=False)
async def telegram_webhook(update: Update):
    create_task(handle_message(update))
    return {"status": "ok"}
