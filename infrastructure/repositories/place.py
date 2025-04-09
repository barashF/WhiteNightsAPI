from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from dal.interfaces.repositories.place import IPlaceRepository
from dal.models.place import Place as PlaceDto
from infrastructure.database.db import get_db
from infrastructure.database.entities.place import Place


class PlaceRepository(IPlaceRepository):
    def __init__(self, db_context: AsyncSession):
        self.db_context = db_context
    
    async def add(self, place: PlaceDto) -> None:
        result = await self.db_context.execute(
            select(Place).where(Place.latitude == place.latitude and
                                Place.longitude == place.longitude and
                                Place.name == place.name))
        entity = result.scalar_one_or_none()
        if entity:
            raise Exception('Место уже зарегистрировано')

        place_entity = self._dto_to_entity(place)
        self.db_context.add(place_entity)
        await self.db_context.commit()
        await self.db_context.refresh(place_entity)
    
    async def get_all(self) -> List[PlaceDto]:
        result = await self.db_context.execute(select(Place))
        places = result.scalars().all()
        return places
        
    def _dto_to_entity(self, dto: PlaceDto) -> Place:
        return Place(**dto)
        

