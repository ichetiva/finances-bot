from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseDAO
from db.models import User


class UserDAO(BaseDAO[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(User, session)

    async def get_by_tg_id(self, user_id: int) -> User:
        _, user = await self.get_or_create(
            for_update=False, id=user_id,
        )
        return user
