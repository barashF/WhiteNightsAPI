from abc import ABC, abstractmethod

from dal.models.group import SGroupInDB, SGroupUpdate


class IGroupRepository(ABC):
    @abstractmethod
    async def add() -> SGroupInDB:
        pass

    @abstractmethod
    async def get(self, group_id: int) -> SGroupInDB:
        pass

    @abstractmethod
    async def delete(self, group_id):
        pass

    @abstractmethod
    async def update(self, data: SGroupUpdate) -> SGroupInDB:
        pass
