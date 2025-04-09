from abc import ABС, abstractmethod
from typing import List, Optional

from dal.models.place import Place


class IPlaceRepository(ABC):
    @abstractmethod
    async def add(self, place: Place) -> None:
        pass

    @abstractmethod
    async def get_place_by_name(self, name: str) -> Optional[Place]:
        pass

