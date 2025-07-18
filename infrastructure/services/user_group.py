from fastapi import HTTPException, status

from dal.models.user_group import UserGroup, UserGroupInDB
from infrastructure.repositories.user_group import UserGroupRepository


class UserGroupService:
    def __init__(self, user_group_repository: UserGroupRepository):
        self.user_group_repository = user_group_repository

    async def join_group(self, user_group: UserGroup) -> UserGroupInDB:
        result = await self.user_group_repository.get(user_group)
        if result:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователь уже состоит в данной группе",
            )
        member = await self.user_group_repository.add(user_group)
        return member
