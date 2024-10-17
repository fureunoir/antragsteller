from aiogram import Bot
from os import getenv

bot = Bot(token=getenv("TELEGRAM_BOT_TOKEN"))
