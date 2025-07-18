from fastapi import HTTPException, status

from dal.interfaces.repositories.group import IGroupRepository
from dal.interfaces.repositories.group_member import IGroupMemberRepository
from dal.interfaces.services.group_member import IGroupMemberService
from dal.models.group import SGroupUpdate
from dal.models.group_member import SGroupMember


class GroupMemberService(IGroupMemberService):
    def __init__(
        self,
        group_member_repository: IGroupMemberRepository,
        group_repository: IGroupRepository,
    ):
        self.group_member_repository = group_member_repository
        self.group_repository = group_repository

    async def kick_member_of_group(self, user_id: int, group_member: SGroupMember):
        group = await self.group_repository.get(group_member.group_id)
        if group.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail="Действие разрешено только владельцу группы",
            )

        await self.group_member_repository.delete(group_member)

    async def leave_from_group(self, group_member: SGroupMember):
        await self.group_member_repository.delete(group_member)
        group = await self.group_repository.get(group_member.group_id)
        list_of_group_members = group.members
        if len(list_of_group_members) == 0:
            await self.group_repository.delete(group.id)
            return

        if group.owner_id == group_member.user_id:
            update_data = SGroupUpdate(owner_id=list_of_group_members[0].id)
            await self.group_repository.update(update_data)
