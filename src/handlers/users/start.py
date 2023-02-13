from aiogram import types

from core.loader import dp
from services import ServicesFactory
from templates import messages, keyboards


@dp.message_handler(commands=["start"])
@dp.message_handler(text="Команды")
async def start(m: types.Message, services: ServicesFactory):
    await services.user_service.get(m.from_user.id)
    await m.answer(messages.START, reply_markup=keyboards.START)
