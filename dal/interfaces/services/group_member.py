from abc import ABC, abstractmethod

from dal.models.group_member import SGroupMember


class IGroupMemberService(ABC):

    @abstractmethod
    async def kick_member_of_group(self, user_id: int, group_member: SGroupMember):
        pass

    @abstractmethod
    async def leave_from_group(self, group_member: SGroupMember):
        pass
