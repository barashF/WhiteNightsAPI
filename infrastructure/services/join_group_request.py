from typing import List

from fastapi import HTTPException, status

from dal.interfaces.services.join_group_request import IJoinGroupRequestService
from dal.models.group_member import SGroupMember
from dal.models.join_group_request import (
    JoinGroupResponse,
    SJoinGroupRequest,
    SJoinGroupRequestInDB,
)
from infrastructure.repositories.group import GroupRepository
from infrastructure.repositories.group_member import GroupMemberRepository
from infrastructure.repositories.join_group_request import JoinGroupRequestRepository


class JoinGroupRequestService(IJoinGroupRequestService):
    def __init__(
        self,
        join_group_request_repository: JoinGroupRequestRepository,
        group_member_repository: GroupMemberRepository,
        group_repository: GroupRepository,
    ):
        self.group_member_repository = group_member_repository
        self.join_group_request_repository = join_group_request_repository
        self.group_repository = group_repository

    async def create_join_group_request(self, request: SJoinGroupRequest):
        result = await self.join_group_request_repository.get_request_by_user_and_group(request)
        if result:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Запрос на вступление уже отправлен",
            )
        member = await self.group_member_repository.get(group_id=request.group_id, user_id=request.user_id)
        if member:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователь уже состоит в группе",
            )

        request_dto = await self.join_group_request_repository.add(request)
        return request_dto

    async def get_list_requests_join_group_by_id(self, owner_id: int, group_id: int) -> List[SJoinGroupRequestInDB]:
        group = await self.group_repository.get(group_id)
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Группа не найдена",
            )
        if group.owner_id != owner_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Пользователь не является владельцем группы",
            )
        requests = await self.join_group_request_repository.get_all_requests_by_group(group_id)
        return requests

    async def response(self, owner_id: int, response: JoinGroupResponse):
        group = await self.group_repository.get(response.group_id)
        if not group:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Группа не найдена",
            )
        if group.owner_id != owner_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Пользователь не является владельцем группы",
            )
        join_request = SJoinGroupRequest(**response.__dict__)
        await self.join_group_request_repository.update_status(response.status, join_request)

        if response.status == "rejected":
            return
        new_group_member = SGroupMember(group_id=response.group_id, user_id=response.user_id)
        await self.group_member_repository.add(new_group_member)
