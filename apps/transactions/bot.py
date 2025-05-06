import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.filters import Command
from aiogram.types.message import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.fsm import FSMContext
from django.core.management import call_command
from django.contrib.auth import get_user_model
import django

# Django configuratsiyasi
django.setup()

# API_TOKEN - BotFather orqali olingan token
API_TOKEN = 'YOUR_BOT_API_TOKEN'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Django'da foydalanuvchi modelini sozlash
User = get_user_model()


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    user, created = User.objects.get_or_create(telegram_id=message.from_user.id)
    if created:
        await message.answer("Siz muvaffaqiyatli ro‘yxatdan o‘tdingiz!")
    else:
        await message.answer("Siz allaqachon ro‘yxatdan o‘tdingiz!")


@dp.message(Command('register'))
async def cmd_register(message: types.Message, state: FSMContext):
    # Foydalanuvchidan login va parolni olish jarayoni
    await message.answer("Loginni kiriting:")
    await state.set_state("waiting_for_login")


@dp.message(state="waiting_for_login")
async def waiting_for_login(message: types.Message, state: FSMContext):
    # Loginni olish
    login = message.text
    await state.update_data(login=login)
    await message.answer("Parolni kiriting:")
    await state.set_state("waiting_for_password")


@dp.message(state="waiting_for_password")
async def waiting_for_password(message: types.Message, state: FSMContext):
    # Parolni olish
    password = message.text
    user_data = await state.get_data()
    login = user_data['login']

    # Foydalanuvchini ro‘yxatdan o‘tkazish
    user = User.objects.create_user(
        telegram_id=message.from_user.id,
        username=login,
        password=password
    )
    await state.finish()  # State to‘xtatish

    await message.answer("Siz muvaffaqiyatli ro‘yxatdan o‘tdingiz!")


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
