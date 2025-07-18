from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dal.interfaces.repositories.group import IGroupRepository
from dal.interfaces.repositories.group_member import IGroupMemberRepository
from dal.interfaces.repositories.join_group_resuest import IJoinGroupRequestRepository
from dal.interfaces.repositories.place import IPlaceRepository
from dal.interfaces.repositories.user import IUserRepository
from dal.interfaces.services.group_member import IGroupMemberService
from dal.interfaces.services.join_group_request import IJoinGroupRequestService
from infrastructure.database.db import get_db
from infrastructure.repositories.group import GroupRepository
from infrastructure.repositories.group_member import GroupMemberRepository
from infrastructure.repositories.join_group_request import JoinGroupRequestRepository
from infrastructure.repositories.place import PlaceRepository
from infrastructure.repositories.user import UserRepository
from infrastructure.services.group_member import GroupMemberService
from infrastructure.services.join_group_request import JoinGroupRequestService
from infrastructure.services.registration import AuthFacade, Validator


def get_user_repository(session: AsyncSession = Depends(get_db)) -> IUserRepository:
    return UserRepository(session)


def get_place_repository(session: AsyncSession = Depends(get_db)) -> IPlaceRepository:
    return PlaceRepository(session)


def get_group_repository(session: AsyncSession = Depends(get_db)) -> IGroupRepository:
    return GroupRepository(session)


def get_join_group_request_repository(
    session: AsyncSession = Depends(get_db),
) -> IJoinGroupRequestRepository:
    return JoinGroupRequestRepository(session)


def get_group_member_repository(
    session: AsyncSession = Depends(get_db),
) -> IGroupMemberRepository:
    return GroupMemberRepository(session)


def get_group_member_service(
    group_member_repository: IGroupMemberRepository = Depends(get_group_member_repository),
    group_repository: IGroupRepository = Depends(get_group_repository),
) -> IGroupMemberService:
    return GroupMemberService(group_member_repository, group_repository)


def get_join_group_request_service(
    join_group_request_repository: IJoinGroupRequestRepository = Depends(get_join_group_request_repository),
    group_member_repository: IGroupMemberRepository = Depends(get_group_member_repository),
    group_repository: IGroupRepository = Depends(get_group_repository),
) -> IJoinGroupRequestService:
    return JoinGroupRequestService(join_group_request_repository, group_member_repository, group_repository)


def get_registration_facade(
    user_repository: IUserRepository = Depends(get_user_repository),
    validator: Validator = Depends(),
) -> AuthFacade:
    return AuthFacade(validator, user_repository)
