from aiogram import types

from core.loader import dp
from services import ServicesFactory
from templates import messages


@dp.message_handler(commands=["/wallets"])
@dp.message_handler(text="Кошельки")
async def wallets_manager(m: types.Message, services: ServicesFactory):
    wallets = await services.wallet_service.get_by_user()
    await m.answer(
        messages.WALLETS.format()
    )
