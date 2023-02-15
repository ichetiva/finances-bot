from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from core.loader import dp
from templates import callbacks, keyboards
from states import CreateWalletState
from services import ServicesFactory
from .wallets import wallets_manager


@dp.callback_query_handler(callbacks.CREATE_WALLET.filter())
async def create_wallet(q: types.CallbackQuery):
    await q.answer("")
    await q.message.answer("Введите название для кошелька",
                           reply_markup=keyboards.BACK_TO_WALLETS)
    await CreateWalletState.name.set()


@dp.message_handler(state=CreateWalletState.name)
async def entered_name(
    m: types.Message,
    services: ServicesFactory,
    state: FSMContext,
):
    wallet_name = m.text
    if len(wallet_name) > 100:
        await m.answer("Слишком длинное название для кошелька")
        return 
    
    await state.finish()
    await services.wallet_service.create(m.from_user.id, wallet_name)
    await wallets_manager(m, services)
