from dao import DAOFactory
from dto import UserDTO
from db import User


class UserService:
    def __init__(self, daos: DAOFactory) -> None:
        self.daos = daos
    
    async def convert_to_dto(self, user: User) -> UserDTO:
        user_dto = UserDTO(
            id=user.id,
            wallets=user.wallets,
        )
        return user_dto
    
    async def get(self, user_id: int) -> UserDTO:
        user = await self.daos.user_dao.get_by_tg_id(user_id)
        return await self.convert_to_dto(user)
