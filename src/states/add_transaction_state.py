from aiogram.dispatcher.filters.state import State, StatesGroup


class AddTransactionState(StatesGroup):
    wallet = State()
    amount = State()
    comment = State()
