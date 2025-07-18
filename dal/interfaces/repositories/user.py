from abc import ABC, abstractmethod
from typing import Optional

from dal.models.user import UserCreate, UserInDB


class IUserRepository(ABC):
    @abstractmethod
    async def add(self, user: UserCreate) -> None:
        pass

    @abstractmethod
    async def get(self, id: int) -> Optional[UserInDB]:
        pass

    @abstractmethod
    async def get_user_by_email(self, email) -> Optional[UserCreate]:
        pass

    @abstractmethod
    async def verify_password(self, password, hashed_password):
        pass
