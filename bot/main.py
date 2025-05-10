# bot/main.py
import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import BOT_TOKEN

# Bot ob'ekti
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# /start komandasi – faqat Telegram ID ni qaytaradi
@dp.message(F.text == "/start")
async def start_handler(message: Message):
    telegram_id = message.from_user.id
    await message.answer(
        f"<b>Sizning Telegram ID'ingiz:</b>\n<code>{telegram_id}</code>\n\n"
        f"Iltimos, ushbu ID ni saytga kiriting."
    )

# start_polling
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
