from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from services import ServicesFactory
from core.loader import dp
from templates import callbacks, keyboards
from states import DeleteWalletState
from .wallets import wallets_manager_callback


@dp.callback_query_handler(callbacks.DELETE_WALLET.filter())
async def delete_wallet(q: types.CallbackQuery, services: ServicesFactory):
    await q.answer("")
    wallets = await services.wallet_service.get_by_user(q.from_user.id)
    await q.message.edit_text("Выберите кошелек")
    await q.message.edit_reply_markup(keyboards.get_wallets_keyboard(wallets))
    await DeleteWalletState.wallet.set()
    

@dp.callback_query_handler(callbacks.WALLET.filter(), state=DeleteWalletState.wallet)
async def entered_wallet(
    q: types.CallbackQuery,
    state: FSMContext,
    callback_data: dict,
):
    await q.answer("")
    await DeleteWalletState.next()
    await state.update_data(wallet_id=int(callback_data["wallet_id"]))
    await q.message.edit_text("Вы уверены?")
    await q.message.edit_reply_markup(keyboards.CONFIRM_DELETE_WALLET)


@dp.callback_query_handler(callbacks.CONFIRM.filter(), state=DeleteWalletState.confirm)
async def confirm_delete_wallet(
    q: types.CallbackQuery,
    services: ServicesFactory,
    state: FSMContext,
):
    await q.answer("")
    async with state.proxy() as data:
        wallet_id = data["wallet_id"]
    await state.finish()
    await services.wallet_service.delete(wallet_id)
    await q.answer("Кошелек удален")
    await wallets_manager_callback(q, services, state)
