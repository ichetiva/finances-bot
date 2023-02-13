from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

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
)
