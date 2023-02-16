from aiogram import types
from aiogram.dispatcher.storage import FSMContext

from core.loader import dp
from services import ServicesFactory
from states import TransactionsState
from templates import callbacks, keyboards, messages

transactions_on_page = 20


@dp.message_handler(text="Транзакции", state="*")
@dp.message_handler(commands=["history"], state="*")
async def list_transactions(
    m: types.Message,
    services: ServicesFactory,
    state: FSMContext
):
    await state.finish()
    wallets = await services.wallet_service.get_by_user(m.from_user.id)
    await m.answer("Выберите кошелек",
                   reply_markup=keyboards.get_wallets_keyboard(wallets))
    await TransactionsState.wallet.set()


@dp.callback_query_handler(callbacks.WALLET.filter(), state=TransactionsState.wallet)
async def entered_wallet(
    q: types.CallbackQuery,
    services: ServicesFactory,
    state: FSMContext,
    callback_data: dict,
):
    await state.finish()
    callback_data.update({"page": 1})
    await paged_transactions(
        q, services, callback_data
    )


@dp.callback_query_handler(callbacks.TRANSACTIONS.filter())
async def paged_transactions(
    q: types.CallbackQuery,
    services: ServicesFactory,
    callback_data: dict,
):
    await q.answer("")
    cur_page = int(callback_data["page"])
    wallet_id = int(callback_data["wallet_id"])
    transactions = (
        await services.transaction_service.get_by_wallet(wallet_id)
    )
    page_transactions = transactions[
        transactions_on_page * cur_page - transactions_on_page:transactions_on_page * cur_page]
    max_page = _get_max_page(len(transactions))
    await q.message.edit_text(
        messages.LIST_TRANSACTIONS.format(
            cur_page=cur_page,
            max_page=max_page,
            transactions="\n\n".join(
                f"- {t.amount} {t.currency}" + (f"\nКомментарий: {t.comment}" if t.comment else "")
                for t in page_transactions
            )
        ),
        reply_markup=keyboards.get_list_transactions_keyboard(wallet_id, cur_page, max_page)
    )


def _get_max_page(transactions_count: int) -> int:
    max_page = transactions_count // transactions_on_page
    if transactions_count % transactions_on_page > 0:
        max_page += 1
    return max_page
