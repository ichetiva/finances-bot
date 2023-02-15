from aiogram.dispatcher.filters.state import State, StatesGroup


class CreateWalletState(StatesGroup):
    name = State()
