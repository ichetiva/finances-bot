import logging
from typing import TYPE_CHECKING

from dao import DAOFactory
from dto import UserDTO
from db import User

if TYPE_CHECKING:
    from services import ServicesFactory


class UserService:
    def __init__(self, services: "ServicesFactory", daos: DAOFactory) -> None:
        self.services = services
        self.daos = daos
    
    def convert_to_dto(self, user: User) -> UserDTO:
        user_dto = UserDTO(
            id=user.id
        )
        return user_dto
    
    async def get(self, user_id: int) -> UserDTO:
        user = await self.daos.user_dao.get_by_tg_id(user_id)
        return self.convert_to_dto(user)
