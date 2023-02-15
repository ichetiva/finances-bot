from aiogram.dispatcher.filters.state import State, StatesGroup


class EditWalletState(StatesGroup):
    wallet = State()
    name = State()
