from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseDAO
from db import Transaction


class TransactionDAO(BaseDAO[Transaction]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Transaction, session)
    
    async def get_by_wallet(self, wallet_id: int) -> list[Transaction]:
        stmt = select(Transaction).where(Transaction.wallet_id == wallet_id)
        transactions = await self.session.scalars(stmt)
        return transactions

    async def create(
        self, wallet_id: int, amount: float, comment: str | None = None,
    ):
        transaction = Transaction(
            wallet_id=wallet_id,
            amount=amount,
            comment=comment,
        )
        self.session.add(transaction)
