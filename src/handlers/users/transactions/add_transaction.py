from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from core.loader import dp
from states import AddTransactionState
from services import ServicesFactory
from templates import keyboards, callbacks
from handlers.users.wallets.wallets import wallets_manager


@dp.message_handler(text="Пополнение", state="*")
@dp.message_handler(text="Оплата", state="*")
async def add_transaction(
    m: types.Message,
    services: ServicesFactory,
    state: FSMContext,
):
    await state.finish()
    wallets = await services.wallet_service.get_by_user(m.from_user.id)
    await m.answer("Выберите кошелек",
                   reply_markup=keyboards.get_wallets_keyboard(wallets))
    await AddTransactionState.wallet.set()

    state = dp.get_current().current_state(user=m.from_user.id)
    if m.text == "Пополнение":
        await state.update_data(t_type="income")
    else:
        await state.update_data(t_type="payment")


@dp.callback_query_handler(callbacks.WALLET.filter(), state=AddTransactionState.wallet)
async def entered_wallet(
    q: types.CallbackQuery,
    state: FSMContext,
    callback_data: dict,
):
    wallet_id = int(callback_data["wallet_id"])
    await state.update_data(wallet_id=wallet_id)
    await q.message.edit_text("Введите сумму")
    await AddTransactionState.next()


@dp.message_handler(state=AddTransactionState.amount)
async def entered_amount(
    m: types.Message,
    state: FSMContext,
):
    try:
        amount = float(m.text)
    except:
        await m.answer("Введите корректную сумму")
        return
    await state.update_data(amount=amount)
    await m.answer("Введите комментарий, если же он не нужен, то напишите просто \"без\"")
    await AddTransactionState.next()


@dp.message_handler(state=AddTransactionState.comment)
async def entered_amount(
    m: types.Message,
    state: FSMContext,
    services: ServicesFactory,
):
    comment = m.text
    if comment.lower() == "без":
        comment = None
    
    async with state.proxy() as data:
        t_type = data["t_type"]
        wallet_id = data["wallet_id"]
        amount = data["amount"]
    await state.finish()
    
    await services.transaction_service.create(
        wallet_id=wallet_id,
        amount=(-1 * amount) if t_type == "payment" else amount,
        comment=comment,
    )

    await m.answer("Транзакция добавлена")
    await wallets_manager(m, services)
