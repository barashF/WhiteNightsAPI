from abc import ABC, abstractmethod
from typing import List

from dal.models.join_group_request import SJoinGroupRequest, SJoinGroupRequestInDB


class IJoinGroupRequestRepository(ABC):
    @abstractmethod
    async def add(self, request: SJoinGroupRequest) -> SJoinGroupRequestInDB:
        pass

    @abstractmethod
    async def get_all_requests_by_group(self, group_id: int) -> List[SJoinGroupRequestInDB]:
        pass
