from sqlalchemy import select
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
