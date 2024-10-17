from aiogram.types import Update

from src.bot import bot


async def handle_start_command(update: Update):
    chat_id = update.message.chat.id
    await bot.send_message(chat_id, "Hello! My name is Antragsteller.\nUse /help to get assistance.")

async def handle_help_command(update: Update):
    chat_id = update.message.chat.id
    await bot.send_message(chat_id, "Here to help! Available commands: /start, /help")

async def handle_message(update: Update):
    if not update.message or not update.message.text:
        return

    if update.message.text == "/start":
        return await handle_start_command(update)
    elif update.message.text == "/help":
        return await handle_help_command(update)
    else:
        chat_id = update.message.chat.id
        await bot.send_message(chat_id, "Unknown command. Use /help for assistance.")
