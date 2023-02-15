from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from dto.wallet import WalletDTO
from . import callbacks

START = (
    ReplyKeyboardMarkup(resize_keyboard=True)
    .add(KeyboardButton("Команды"))
    .add(KeyboardButton("Пополнение"), KeyboardButton("Оплата"))
    .add(KeyboardButton("Кошельки"))
    .add(KeyboardButton("Транзакции"))
)

WALLETS = (
    InlineKeyboardMarkup()
    .add(InlineKeyboardButton("Создать", callback_data=callbacks.CREATE_WALLET.new()))
    .add(InlineKeyboardButton("Изменить", callback_data=callbacks.EDIT_WALLET.new()))
    .add(InlineKeyboardButton("Удалить", callback_data=callbacks.DELETE_WALLET.new()))
    .add(InlineKeyboardButton("В меню", callback_data=callbacks.MENU.new()))
)

BACK_TO_WALLETS = (
    InlineKeyboardMarkup()
    .add(InlineKeyboardButton("В начало", callback_data=callbacks.WALLETS.new()))
)

CONFIRM_DELETE_WALLET = (
    InlineKeyboardMarkup()
    .add(
        InlineKeyboardButton(
            "Удалить", callback_data=callbacks.CONFIRM.new(),
        ),
        InlineKeyboardButton(
            "Отмена", callback_data=callbacks.WALLETS.new(),
        )
    )
)


def get_wallets_keyboard(wallets: list[WalletDTO]):
    keyboard = InlineKeyboardMarkup()
    for wallet in wallets:
        keyboard.add(
            InlineKeyboardButton(wallet.name,
                                 callback_data=callbacks.WALLET.new(wallet_id=wallet.id))
        )
    return keyboard
