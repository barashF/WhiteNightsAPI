from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from dal.interfaces.repositories.place import IPlaceRepository
from dal.models.place import Place as PlaceDto
from dal.models.place import PlaceInDB, PlaceUpdate
from infrastructure.database.entities.models import Place


class PlaceRepository(IPlaceRepository):
    def __init__(self, db_context: AsyncSession):
        self.db_context = db_context

    async def add(self, place: PlaceDto) -> PlaceDto:
        result = await self.db_context.execute(
            select(Place).where(
                Place.latitude == place.latitude and Place.longitude == place.longitude and Place.name == place.name
            )
        )
        entity = result.scalar_one_or_none()
        if entity:
            raise Exception("Место уже зарегистрировано")

        place_entity = self._dto_to_entity(place)
        self.db_context.add(place_entity)
        await self.db_context.commit()
        await self.db_context.refresh(place_entity)
        return self._entity_to_dto(place_entity)

    async def get_place_by_name(self, name: str) -> PlaceInDB:
        result = await self.db_context.execute(select(Place).where(Place.name == name))
        entity = result.scalar_one_or_none()
        if not entity:
            raise Exception("Заведение не найдено")
        return self._entity_to_dto(entity)

    async def get_all(self) -> List[PlaceDto]:
        result = await self.db_context.execute(select(Place))
        places = result.scalars().all()
        return places

    async def update(self, place_id: int, place_update: PlaceUpdate):
        entity = await self.db_context.get(Place, place_id)
        if not entity:
            raise HTTPException(status_code=404, detail="Завдение не найдено")

        entity.update(**place_update.__dict__)
        await self.db_context.commit()
        await self.db_context.refresh(entity)

        return self._entity_to_dto(entity)

    def _dto_to_entity(self, dto: PlaceDto) -> Place:
        return Place(**dto.__dict__)

    def _entity_to_dto(self, entity: Place) -> PlaceInDB:
        return PlaceInDB(**entity.__dict__)
