import logging
import os
import asyncio
import sys
import django
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from django.contrib.auth import get_user_model

# Loyiha ildiz katalogini Python yo'liga qo'shish
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

# DJANGO_SETTINGS_MODULE ni sozlash
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Django'ni sozlash
try:
    django.setup()
except Exception as e:
    raise ImportError(f"Django sozlamalarini yuklashda xatolik: {e}")
# # Bot tokenini environmentdan olish
# API_TOKEN = os.getenv("BOT_API_TOKEN")
# if not API_TOKEN:
#     raise ValueError("BOT_API_TOKEN environment o'zgaruvchisi aniqlanmadi!")

logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher yaratish
API_TOKEN = "7305620237:AAH6PZheLJKCAOrHuy66rixGmR-X3clYRx0"
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


# Maxsus holatlar guruhi
class RegistrationStates(StatesGroup):
    waiting_for_login = State()
    waiting_for_password = State()


# Django foydalanuvchi modeli
User = get_user_model()


# /start komandasi uchun handler
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    # Telegram ID orqali foydalanuvchini yaratish yoki olish
    user, created = User.objects.get_or_create(telegram_id=message.from_user.id)
    if created:
        await message.answer("Siz muvaffaqiyatli ro‘yxatdan o‘tdingiz!")
    else:
        await message.answer("Siz allaqachon ro‘yxatdan o‘tdingiz!")


# /register komandasi uchun handler
@dp.message(Command("register"))
async def cmd_register(message: types.Message, state: FSMContext):
    await message.answer("Loginni kiriting:")
    await state.set_state(RegistrationStates.waiting_for_login)


# Loginni kutish
@dp.message(RegistrationStates.waiting_for_login)
async def waiting_for_login(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer("Parolni kiriting:")
    await state.set_state(RegistrationStates.waiting_for_password)


# Parolni kutish
@dp.message(RegistrationStates.waiting_for_password)
async def waiting_for_password(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    login = user_data["login"]
    password = message.text

    user = User.objects.create_user(
        telegram_id=message.from_user.id,
        username=login,
        password=password
    )
    await state.clear()  # Holatni tozalash
    await message.answer("Siz muvaffaqiyatli ro‘yxatdan o‘tdingiz!")


# Botni ishga tushirish
if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot, skip_updates=True))
