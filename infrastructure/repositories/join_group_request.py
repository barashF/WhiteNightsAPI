from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from dal.interfaces.repositories.join_group_resuest import IJoinGroupRequestRepository
from dal.models.join_group_request import SJoinGroupRequest, SJoinGroupRequestInDB
from infrastructure.database.entities.models import Group, JoinGroupRequest, User


class JoinGroupRequestRepository(IJoinGroupRequestRepository):
    def __init__(self, db_context: AsyncSession):
        self.db_context = db_context

    async def add(self, request: SJoinGroupRequest) -> SJoinGroupRequestInDB:
        group = await self.db_context.get(Group, request.group_id)
        user = await self.db_context.get(User, request.user_id)
        if not group or not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="группа или пользователь не найдены",
            )

        request_entity = self._dto_to_entity(request)
        self.db_context.add(request_entity)
        await self.db_context.commit()
        await self.db_context.refresh(request_entity)
        request_dto = self._entity_to_dto(request_entity)
        return request_dto

    async def get_all_requests_by_group(self, group_id):
        result = await self.db_context.execute(
            select(JoinGroupRequest).where(
                JoinGroupRequest.group_id == group_id,
                JoinGroupRequest.status == "expectation",
            )
        )
        requests = result.scalars().all()
        return [self._entity_to_dto(request) for request in requests]

    async def get_request_by_user_and_group(self, request: SJoinGroupRequest):
        result = await self.db_context.execute(
            select(JoinGroupRequest).where(
                JoinGroupRequest.group_id == request.group_id,
                JoinGroupRequest.user_id == request.user_id,
                JoinGroupRequest.status == "expectation",
            )
        )
        request = result.scalar_one_or_none()
        if not request:
            return request
        return self._entity_to_dto(request)

    async def update_status(self, status_request: str, data: SJoinGroupRequest):
        result = await self.db_context.execute(
            select(JoinGroupRequest).where(
                JoinGroupRequest.group_id == data.group_id,
                JoinGroupRequest.user_id == data.user_id,
                JoinGroupRequest.status == "expectation",
            )
        )
        request = result.scalar_one_or_none()
        if not request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Запрос на вступление не найден",
            )
        request.status = status_request
        await self.db_context.commit()
        await self.db_context.refresh(request)
        request_dto = self._entity_to_dto(request)
        return request_dto

    def _dto_to_entity(self, dto: SJoinGroupRequest) -> JoinGroupRequest:
        return JoinGroupRequest(**dto.__dict__)

    def _entity_to_dto(self, entity: JoinGroupRequest) -> SJoinGroupRequestInDB:
        return SJoinGroupRequestInDB(**entity.__dict__)
