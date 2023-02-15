from aiogram.dispatcher.filters.state import State, StatesGroup


class DeleteWalletState(StatesGroup):
    wallet = State()
    confirm = State()
