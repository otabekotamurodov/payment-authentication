# === bot/main.py ===
import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiohttp import web
from config import BOT_TOKEN

# Bot obyekti
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Telegramdan kirgan start komandasi
@dp.message(F.text == "/start")
async def start_handler(message: Message):
    telegram_id = message.from_user.id
    await message.answer(
        f"<b>Sizning Telegram ID'ingiz:</b>\n<code>{telegram_id}</code>\n\n"
        f"Iltimos, ushbu ID ni saytga kiriting."
    )

# Tashqi so'rov orqali xabar yuborish (REST)
routes = web.RouteTableDef()

@routes.post('/send_code')
async def send_code(request):
    data = await request.json()
    telegram_id = data.get("telegram_id")
    code = data.get("code")

    if not telegram_id or not code:
        return web.json_response({"error": "Missing fields"}, status=400)

    try:
        await bot.send_message(
            chat_id=telegram_id,
            text=f"<b>Sizning tasdiqlash kodingiz:</b> <code>{code}</code>\n\nKod 5 daqiqa amal qiladi."
        )
        return web.json_response({"message": "Yuborildi"})
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)

# Botni ishga tushurish
async def main():
    logging.basicConfig(level=logging.INFO)

    # Bot polling
    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling(bot))

    # API server
    app = web.Application()
    app.add_routes(routes)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "localhost", 8081)
    await site.start()

    print("Bot va REST API server ishga tushdi")
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())