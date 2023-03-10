from sqlalchemy.ext.asyncio import AsyncSession

from dao import DAOFactory
from .user import UserService
from .wallet import WalletService
from .transaction import TransactionService


class ServicesFactory:
    def __init__(self, session: AsyncSession) -> None:
        self.daos = DAOFactory(session)
    
    @property
    def user_service(self):
        return UserService(self, self.daos)
    
    @property
    def wallet_service(self):
        return WalletService(self.daos)
    
    @property
    def transaction_service(self):
        return TransactionService(self, self.daos)
