from aiogram import Bot
from os import getenv

from sentry_sdk import capture_exception

from src.logging import logger

bot = Bot(token=getenv("TELEGRAM_BOT_TOKEN"))

async def set_antragsteller_webhook():
    try:

        await bot.set_webhook(getenv("TELEGRAM_WEBHOOK_URL") + getenv("TELEGRAM_BOT_TOKEN").split(":")[1])

    except Exception as telegram_exception:

        capture_exception(telegram_exception)

        logger.warning("Something went wrong while setting bot's webhook: %s", telegram_exception)
