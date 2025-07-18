from abc import ABC, abstractmethod

from dal.models.group_member import SGroupMember


class IGroupMemberRepository(ABC):
    @abstractmethod
    async def add(self, group_member: SGroupMember):
        pass

    @abstractmethod
    async def get(self, group_id: int, user_id: int):
        pass

    @abstractmethod
    async def delete(self, group_id: int, user_id: int):
        pass
