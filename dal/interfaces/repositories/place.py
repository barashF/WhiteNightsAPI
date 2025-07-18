from abc import ABC, abstractmethod
from typing import Optional

from dal.models.place import Place, PlaceInDB


class IPlaceRepository(ABC):
    @abstractmethod
    async def add(self, place: Place) -> None:
        pass

    @abstractmethod
    async def get_place_by_name(self, name: str) -> Optional[PlaceInDB]:
        pass
