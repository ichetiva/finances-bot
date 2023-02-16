from typing import TYPE_CHECKING

from dao import DAOFactory
from dto import TransactionDTO
from db import Transaction

if TYPE_CHECKING:
    from . import ServicesFactory


class TransactionService:
    def __init__(self, services: "ServicesFactory", daos: DAOFactory) -> None:
        self.services = services
        self.daos = daos
    
    def convert_to_dto(self, transaction: Transaction, currency: str) -> TransactionDTO:
        transaction_dto = TransactionDTO(
            id=transaction.id,
            wallet_id=transaction.wallet_id,
            amount=transaction.amount,
            currency=currency,
            comment=transaction.comment,
            created_at=transaction.created_at,
        )
        return transaction_dto
    
    def convert_multiple_to_dto(
        self, transactions: list[Transaction], currency: str
    ) -> list[TransactionDTO]:
        transactions_dto = []
        for transaction in transactions:
            transactions_dto.append(self.convert_to_dto(transaction, currency))
        return transactions_dto
    
    async def create(
        self, wallet_id: int, amount: float, comment: str | None = None,
    ):
        await self.daos.transaction_dao.create(wallet_id, amount, comment)
        await self.daos.wallet_dao.update_balance(wallet_id, amount)
        await self.daos.session.commit()

    async def get_by_wallet(
        self, wallet_id: int,
    ):
        currency = await self.services.wallet_service.get_currency_by_wallet(wallet_id)
        transactions = await self.daos.transaction_dao.get_by_wallet(wallet_id)
        return self.convert_multiple_to_dto(transactions, currency)
