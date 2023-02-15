import logging
from typing import Generic, Type, TypeVar

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Base

Model = TypeVar("Model", bound=Base)


class BaseDAO(Generic[Model]):
    def __init__(self, model: Type[Model], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get_all(self) -> list[Model]:
        stmt = select(self.model)
        instances = await self.session.scalars(stmt).all()
        return instances
    
    async def get(self, for_update: bool = False, **kwargs) -> Model | None:
        stmt = select(self.model).filter_by(**kwargs)
        if for_update:
            stmt = stmt.with_for_update()
        instance = await self.session.execute(stmt)
        return instance.scalar_one_or_none()
    
    async def get_or_create(
        self,
        defaults: dict = {},
        for_update: bool = False,
        **kwargs
    ) -> tuple[bool, Model]:
        instance = await self.get(for_update, **kwargs)
        if instance:
            return False, instance
        kwargs.update(defaults)
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.commit()
        return True, instance
    
    async def single_update(
        self, instance: Type[Model], **kwargs
    ):
        stmt = update(self.model).where(self.model.id == instance.id).values(**kwargs)
        await self.session.execute(stmt)
        await self.session.commit()
