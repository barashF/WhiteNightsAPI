from enum import Enum

from pydantic import BaseModel


class SJoinGroupRequest(BaseModel):
    user_id: int
    group_id: int


class SJoinGroupRequestInDB(SJoinGroupRequest):
    id: int
    status: str


class ResponseStatus(str, Enum):
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class JoinGroupResponse(SJoinGroupRequest):
    status: ResponseStatus
