from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from dal.models.user_group import UserGroup, UserGroupInDB
from infrastructure.database.entities.models import Group_Member


class UserGroupRepository:
    def __init__(self, db_context: AsyncSession):
        self.db_context = db_context

    async def add(self, user_group: UserGroup) -> UserGroupInDB:
        member = await self._dto_to_entity(user_group)
        self.db_context.add(user_group)
        await self.db_context.commit()
        await self.db_context.refresh(member)
        member_dto = await self._entity_to_dto(member)
        return member_dto

    async def get(self, user_group: UserGroup) -> UserGroupInDB:
        member = await self.db_context.execute(
            select(UserGroup).where(
                UserGroup.user_id == user_group.user_id and UserGroup.group_id == user_group.group_id
            )
        ).scalar_one_or_none()
        member_dto = await self._entity_to_dto(member)
        return member_dto

    async def _dto_to_entity(self, dto: UserGroup) -> Group_Member:
        return Group_Member(**dto.__dict__)

    async def _entity_to_dto(self, entity: Group_Member) -> UserGroupInDB:
        return UserGroupInDB(**entity.__dict__)
