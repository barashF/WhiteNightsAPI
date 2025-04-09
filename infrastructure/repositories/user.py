from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from dal.interfaces.repositories.user import IUserRepository
from dal.models.user import (
    UserCreate, UserInDB, UserUpdate
    )
from infrastructure.database.entities.user import User


class UserRepository(IUserRepository):
    def __init__(self, db_context: AsyncSession):
        self.db_context = db_context
    
    async def add(self, user: UserCreate) -> User:
        result = await self.db_context.execute(
            select(User).where(User.email == user.email))
        entity = result.scalars_one_or_none()
        if entity:
            raise Exception('Данная почта уже зарегистрирована')

        user_entity = self._dto_to_entity(user)
        self.db_context.add(user_entity)
        await self.db_context.commit()
        await self.db_context.refresh(user_entity)
        return user_entity

    async def get(self):
        pass
    
    def _dto_to_entity(self, dto: UserCreate) -> User:
        return User(**dto)