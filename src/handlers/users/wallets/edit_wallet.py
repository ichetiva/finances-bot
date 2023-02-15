from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from core.loader import dp
from templates import callbacks, keyboards
from services import ServicesFactory
from states import EditWalletState
from .wallets import wallets_manager


@dp.callback_query_handler(callbacks.EDIT_WALLET.filter())
async def edit_wallet(q: types.CallbackQuery, services: ServicesFactory):
    await q.answer("")
    wallets = await services.wallet_service.get_by_user(q.from_user.id)
    await q.message.edit_text("Выберите кошелек")
    await q.message.edit_reply_markup(keyboards.get_wallets_keyboard(wallets))
    await EditWalletState.wallet.set()


@dp.callback_query_handler(callbacks.WALLET.filter(), state=EditWalletState.wallet)
async def entered_wallet(
    q: types.CallbackQuery,
    state: FSMContext,
    callback_data: dict,
):
    await q.answer("")
    await state.update_data(wallet_id=int(callback_data["wallet_id"]))
    await q.message.edit_text("Введите новое название")
    await q.message.edit_reply_markup(keyboards.BACK_TO_WALLETS)
    await EditWalletState.name.set()


@dp.message_handler(state=EditWalletState.name)
async def entered_name(
    m: types.Message,
    services: ServicesFactory,
    state: FSMContext,
):
    wallet_name = m.text
    if len(wallet_name) > 100:
        await m.answer("Слишком длинное название для кошелька")
        return

    async with state.proxy() as data:
        wallet_id = data["wallet_id"]
    await state.finish()
    await services.wallet_service.edit_name(wallet_id, wallet_name)
    await wallets_manager(m, services)
