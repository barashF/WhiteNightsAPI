from abc import ABC, abstractmethod
from typing import List

from dal.models.join_group_request import JoinGroupResponse, SJoinGroupRequest


class IJoinGroupRequestService(ABC):
    @abstractmethod
    async def create_join_group_request(self, request: SJoinGroupRequest):
        pass

    @abstractmethod
    async def get_list_requests_join_group_by_id(self, owner_id: int, group_id: int) -> List[SJoinGroupRequest]:
        pass

    @abstractmethod
    async def response(self, owner_id: int, response: JoinGroupResponse):
        pass
