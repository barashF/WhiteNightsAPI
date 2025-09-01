from typing import List, Optional

from fastapi import APIRouter, Depends

from application.di import (
    get_group_member_repository,
    get_group_member_service,
    get_group_repository,
    get_join_group_request_service,
)
from dal.interfaces.repositories.group import IGroupRepository
from dal.interfaces.repositories.group_member import IGroupMemberRepository
from dal.interfaces.services.group_member import IGroupMemberService
from dal.interfaces.services.join_group_request import IJoinGroupRequestService
from dal.models.group import SGroup, SGroupInDB
from dal.models.group_member import SGroupMember
from dal.models.join_group_request import (
    JoinGroupResponse,
    SJoinGroupRequest,
    SJoinGroupRequestInDB,
)
from dal.models.user import UserInDB
from infrastructure.services.auth import get_current_user


router = APIRouter(prefix="/group", tags=["Group"])


@router.post("/create_group")
async def create_group(
    group: SGroup,
    current_user: UserInDB = Depends(get_current_user),
    group_repository: IGroupRepository = Depends(get_group_repository),
    group_member_repository: IGroupMemberRepository = Depends(get_group_member_repository),
) -> SGroupInDB:
    group_create: SGroupInDB = await group_repository.add(group, current_user.id)
    group_member = SGroupMember(user_id=group_create.owner_id, group_id=group_create.id)
    await group_member_repository.add(group_member)
    return group_create


@router.get("/get_group/{group_id}")
async def get_group(
    group_id: int, group_repository: IGroupRepository = Depends(get_group_repository)
) -> Optional[SGroupInDB]:
    group = await group_repository.get(group_id)
    return group


@router.post("/leave/{group_id}")
async def leave_from_group(
    group_id: int,
    current_user: UserInDB = Depends(get_current_user),
    group_member_service: IGroupMemberService = Depends(get_group_member_service),
):
    group_member = SGroupMember(user_id=current_user.id, group_id=group_id)
    await group_member_service.leave_from_group(group_member)


@router.post("/kick")
async def kick_member_of_group(
    group_member: SGroupMember,
    current_user: UserInDB = Depends(get_current_user),
    group_member_service: IGroupMemberService = Depends(get_group_member_service),
):
    await group_member_service.kick_member_of_group(current_user.id, group_member)


@router.post("/request_join_group")
async def create_request(
    group_id: int,
    current_user: UserInDB = Depends(get_current_user),
    join_group_request_service: IJoinGroupRequestService = Depends(get_join_group_request_service),
):
    request = SJoinGroupRequest(group_id=group_id, user_id=current_user.id)
    await join_group_request_service.create_join_group_request(request)


@router.get("/request_join_group/list_requests/{group_id}")
async def get_requests(
    group_id: int,
    current_user: UserInDB = Depends(get_current_user),
    join_group_request_service: IJoinGroupRequestService = Depends(get_join_group_request_service),
) -> List[SJoinGroupRequestInDB]:
    requests = await join_group_request_service.get_list_requests_join_group_by_id(current_user.id, group_id)
    return requests


@router.post("/request_join_group/response")
async def response(
    response: JoinGroupResponse,
    current_user: UserInDB = Depends(get_current_user),
    join_group_request_service: IJoinGroupRequestService = Depends(get_join_group_request_service),
):
    await join_group_request_service.response(current_user.id, response)
