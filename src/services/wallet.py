from dao import DAOFactory
from db import Wallet
from dto import WalletDTO


class WalletService:
    def __init__(self, daos: DAOFactory) -> None:
        self.daos = daos

    def convert_to_dto(self, wallet: Wallet) -> WalletDTO:
        wallet_dto = WalletDTO(
            id=wallet.id,
            user_id=wallet.user_id,
            name=wallet.name,
            balance=wallet.balance,
            currency=wallet.currency,
        )
        return wallet_dto

    def convert_multiple_to_dto(self, wallets: list[Wallet]) -> list[WalletDTO]:
        list_wallet_dto = []
        for wallet in wallets:
            list_wallet_dto.append(self.convert_to_dto(wallet))
        return list_wallet_dto
    
    async def get_by_user(self, user_id: int):
        wallets = await self.daos.wallet_dao.get_by_tg_id(user_id)
        return wallets
