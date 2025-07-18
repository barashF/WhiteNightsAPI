from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from .place import PlaceInDB
from .user import UserInDB


class SGroup(BaseModel):
    datetime: datetime
    place_id: Optional[int] = None
    event_id: Optional[int] = None


class SGroupCreate(SGroup):
    owner_id: int


class SGroupInDB(SGroup):
    id: int
    owner_id: int
    place: Optional[PlaceInDB] = None
    members: Optional[List[UserInDB]] = None


class SGroupUpdate(SGroup):
    owner_id: Optional[int] = None
    datetime: Optional[datetime] = None
