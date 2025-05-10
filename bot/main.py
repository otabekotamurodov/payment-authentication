# bot/main.py
import asyncio
import random
import logging
import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties  # Yangi import
from config import BOT_TOKEN, DJANGO_BACKEND_URL

# Bot ob'ektini DefaultBotProperties bilan yaratish
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


@dp.message(F.text == "/start")
async def start_handler(message: Message):
    telegram_id = message.from_user.id
    code = str(random.randint(100000, 999999))

    # Kodni backendga jo‘natish
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{DJANGO_BACKEND_URL}/api/auth/generate-code/", json={
            "telegram_id": telegram_id
        }) as resp:
            if resp.status == 200:
                await message.answer(
                    f"<b>Telegram orqali login kodi:</b>\n<code>{code}</code>\n\nKod 5 daqiqa amal qiladi.")
            else:
                await message.answer("Xatolik yuz berdi. Iltimos, qayta urinib ko‘ring.")


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
