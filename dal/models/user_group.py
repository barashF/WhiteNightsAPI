from pydantic import BaseModel


class UserGroup(BaseModel):
    group_id: int
    user_id: int


class UserGroupInDB(UserGroup):
    id: int
