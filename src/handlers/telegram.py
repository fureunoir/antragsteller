from asyncio import create_task
from os import getenv

from aiogram.types import Update

from src.handlers import router
from src.helpers.bot import handle_message

verify = getenv("TELEGRAM_BOT_TOKEN").split(":")[1]

@router.post("/webhook/{url_part}", include_in_schema=False)
async def telegram_webhook(url_part: str, update: Update):
    if not url_part == verify:
        return {"status": "get outta here"}
    create_task(handle_message(update))
    return {"status": "ok"}
