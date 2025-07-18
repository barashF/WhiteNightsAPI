from pydantic import BaseModel


class SGroupMember(BaseModel):
    user_id: int
    group_id: int
