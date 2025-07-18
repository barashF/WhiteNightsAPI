from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dal.interfaces.repositories.group_member import IGroupMemberRepository
from dal.models.group_member import SGroupMember
from infrastructure.database.entities.models import Group_Member


class GroupMemberRepository(IGroupMemberRepository):
    def __init__(self, db_context: AsyncSession):
        self.db_context = db_context

    async def add(self, group_member: SGroupMember) -> SGroupMember:
        group_member_entity = await self._dto_to_entity(group_member)
        self.db_context.add(group_member_entity)
        await self.db_context.commit()
        await self.db_context.refresh(group_member_entity)
        group_member_dto = await self._entity_to_dto(group_member_entity)
        return group_member_dto

    async def get(self, group_id: int, user_id: int) -> Optional[SGroupMember | None]:
        result = await self.db_context.execute(
            select(Group_Member).where(Group_Member.group_id == group_id, Group_Member.user_id == user_id)
        )
        group_member_entity = result.scalar_one_or_none()
        if not group_member_entity:
            return None
        return SGroupMember(**group_member_entity.__dict__)

    async def delete(self, group_member: SGroupMember):
        result = await self.db_context.execute(
            select(Group_Member).where(
                Group_Member.group_id == group_member.group_id,
                Group_Member.user_id == group_member.user_id,
            )
        )
        group_member_entity = result.scalar_one_or_none()
        if group_member_entity is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Участник группы не был найден",
            )
        await self.db_context.delete(group_member_entity)
        await self.db_context.commit()

    async def _dto_to_entity(self, dto: SGroupMember) -> Group_Member:
        return Group_Member(**dto.__dict__)

    async def _entity_to_dto(self, entity: Group_Member) -> SGroupMember:
        return SGroupMember(**entity.__dict__)
