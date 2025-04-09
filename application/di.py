from infrastructure.database.db import get_db
from infrastructure.repositories.user import UserRepository
from dal.interfaces.repositories.user import IUserRepository

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


def get_user_repository(session: AsyncSession = Depends(get_db)) -> IUserRepository:
    return UserRepository(session)