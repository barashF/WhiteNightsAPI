from typing import List, Optional

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from dal.interfaces.repositories.user import IUserRepository
from dal.models.user import UserAuth, UserCreate, UserInDB
from infrastructure.database.entities.models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")


class UserRepository(IUserRepository):
    def __init__(self, db_context: AsyncSession):
        self.db_context = db_context
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, password, hashed_password):
        return self.pwd_context.verify(password, hashed_password)

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    async def add(self, user: UserCreate) -> UserInDB:
        result = await self.db_context.execute(select(User).where(User.email == user.email))
        entity = result.scalar_one_or_none()
        if entity:
            raise Exception("Данная почта уже зарегистрирована")

        user_entity = self._dto_to_entity(user)
        user_entity.password = self.get_password_hash(user_entity.password)
        self.db_context.add(user_entity)
        await self.db_context.commit()
        await self.db_context.refresh(user_entity)
        return self._entity_to_dto(user_entity)

    async def get(self, user_id: int) -> Optional[UserInDB]:
        result = await self.db_context.execute(select(User).where(User.id == user_id))
        entity = result.scalar_one_or_none()
        if entity is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

        dto_user = self._entity_to_dto(entity)
        return dto_user

    async def get_user_by_email(self, email: str, model: BaseModel) -> Optional[UserInDB | UserAuth]:
        result = await self.db_context.execute(select(User).where(User.email == email))
        entity = result.scalar_one_or_none()
        if entity is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

        return model(**entity.__dict__)

    async def get_all_users(self) -> List[UserInDB]:
        result = await self.db_context.execute(select(User))
        entities = result.scalars().all()
        return self._entity_to_list_dto(entities)

    def _dto_to_entity(self, dto: UserCreate) -> User:
        return User(**dto.model_dump())

    def _entity_to_dto(self, user: User) -> UserInDB:
        return UserInDB(**user.__dict__)

    def _entity_to_list_dto(self, entities: List[User]) -> List[UserInDB]:
        return [UserInDB.model_validate(entity) for entity in entities]
