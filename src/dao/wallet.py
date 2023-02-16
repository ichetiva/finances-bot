from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseDAO
from db import Wallet


class WalletDAO(BaseDAO[Wallet]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Wallet, session)

    async def get_by_tg_id(self, user_id: int) -> list[Wallet]:
        stmt = select(Wallet).where(Wallet.user_id == user_id)
        wallets = (await self.session.scalars(stmt)).all()
        return wallets
    
    async def create(self, user_id: int, name: str):
        wallet = Wallet(user_id=user_id, name=name, currency="RUB")
        self.session.add(wallet)
        await self.session.commit()
    
    async def delete(self, wallet_id: int):
        stmt = delete(Wallet).where(Wallet.id == wallet_id)
        await self.session.execute(stmt)
        await self.session.commit()
    
    async def update_balance(self, wallet_id: int, amount: float):
        wallet = await self.get(for_update=True, id=wallet_id)
        wallet.balance += amount
    
    async def get_currency_by_wallet(self, wallet_id: int) -> str:
        stmt = select(Wallet.currency).where(Wallet.id == wallet_id)
        currency = await self.session.scalar(stmt)
        return currency
