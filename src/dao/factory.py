from sqlalchemy.ext.asyncio import AsyncSession

from .user import UserDAO
from .wallet import WalletDAO


class DAOFactory:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    
    @property
    def user_dao(self):
        return UserDAO(self.session)
    
    @property
    def wallet_dao(self):
        return WalletDAO(self.session)
