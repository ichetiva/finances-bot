from aiogram import types

from core.loader import dp
from services import ServicesFactory
from templates import messages, keyboards, callbacks


@dp.message_handler(commands=["start"])
@dp.message_handler(text="Команды")
async def start(m: types.Message, services: ServicesFactory):
    await services.user_service.get(m.from_user.id)
    await m.answer(messages.START, reply_markup=keyboards.START)


@dp.callback_query_handler(callbacks.MENU.filter())
async def start_callback(q: types.CallbackQuery):
    await q.message.answer(messages.START, reply_markup=keyboards.START)
