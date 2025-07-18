from datetime import datetime, timezone
from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from dal.interfaces.repositories.group import IGroupRepository
from dal.models.group import SGroup, SGroupCreate, SGroupInDB, SGroupUpdate
from dal.models.user import UserInDB
from infrastructure.database.entities.models import Group


class GroupRepository(IGroupRepository):
    def __init__(self, db_context: AsyncSession):
        self.db_context = db_context

    async def add(self, group: SGroup, user_id: int) -> SGroupInDB:
        if group.datetime.astimezone(timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The specified date is in the past",
            )
        group_create = SGroupCreate(**group.__dict__, owner_id=user_id)
        group_entity = await self._dto_to_entity(group_create)
        self.db_context.add(group_entity)
        await self.db_context.commit()
        await self.db_context.refresh(group_entity)
        group_dto = await self._entity_to_dto(group_entity)
        return group_dto

    async def get(self, group_id: int) -> SGroupInDB:
        result = await self.db_context.execute(
            select(Group).options(selectinload(Group.members)).where(Group.id == group_id)
        )
        group_entity = result.scalar_one_or_none()
        if not group_entity:
            return None
        group_dto = await self._entity_to_dto(group_entity)
        return group_dto

    async def delete(self, group_id: int):
        result = await self.db_context.get(Group, group_id)
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
        await self.db_context.delete(result)
        await self.db_context.commit()

    async def get_members_by_id(self, group_id: int) -> Optional[List[UserInDB]]:
        group = await self.db_context.get(Group, group_id)
        if not group:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
        members = group.members
        return [UserInDB(**member.__dict__) for member in members]

    async def update(self, group_id: int, data: SGroupUpdate) -> SGroupInDB:
        group = await self.db_context.get(Group, group_id)
        if not group:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
        group_data = data.dict(exclude_unset=True)
        for field, value in group_data.items():
            if hasattr(group, field):
                setattr(group, field, value)
        await self.db_context.commit()
        await self.db_context.refresh(group)
        group_dto = await self._entity_to_dto(group)
        return group_dto

    async def _dto_to_entity(self, dto: SGroupCreate) -> Group:
        return Group(**dto.__dict__)

    async def _entity_to_dto(self, entity: Group) -> SGroupInDB:
        return SGroupInDB(**entity.__dict__)
