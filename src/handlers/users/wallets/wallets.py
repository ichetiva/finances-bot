from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from dto import WalletDTO
from core.loader import dp
from services import ServicesFactory
from templates import messages, keyboards, callbacks


@dp.message_handler(commands=["/wallets"])
@dp.message_handler(text="Кошельки")
async def wallets_manager(m: types.Message, services: ServicesFactory):
    wallets = await services.wallet_service.get_by_user(m.from_user.id)
    message = _get_message(wallets)
    await m.answer(message, reply_markup=keyboards.WALLETS)
    

@dp.callback_query_handler(callbacks.WALLETS.filter(), state="*")
async def wallets_manager_callback(
    q: types.CallbackQuery,
    services: ServicesFactory,
    state: FSMContext,
):
    await q.answer("")
    await state.finish()
    wallets = await services.wallet_service.get_by_user(q.from_user.id)
    message = _get_message(wallets)
    await q.message.edit_text(message)
    await q.message.edit_reply_markup(keyboards.WALLETS)
    

def _get_message(wallets: list[WalletDTO]):
    if len(wallets) > 0:
        wallets_string = "\n".join(
            f"{idx}. {wallet.name}, {wallet.balance} {wallet.currency}"
            for idx, wallet in enumerate(wallets, 1)
        )
    else:
        wallets_string = "Не найдено"
    message = messages.WALLETS.format(wallets=wallets_string)
    return message
