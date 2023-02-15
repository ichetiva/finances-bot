from aiogram.utils.callback_data import CallbackData

MENU = CallbackData("menu")
CREATE_WALLET = CallbackData("create_wallet")
EDIT_WALLET = CallbackData("edit_wallet")
DELETE_WALLET = CallbackData("delete_wallet")
WALLETS = CallbackData("wallets")
WALLET = CallbackData("wallet", "wallet_id")
CONFIRM = CallbackData("confirm")
