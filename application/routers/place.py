from fastapi import APIRouter, Depends

from application.di import get_place_repository
from dal.models.place import Place as PlaceDto
from dal.models.place import PlaceInDB, PlaceUpdate
from infrastructure.repositories.place import PlaceRepository


router = APIRouter(prefix="/place", tags=["Place"])


@router.post("/add_place", summary="Добавление локации")
async def add_place(place: PlaceDto, place_repository: PlaceRepository = Depends(get_place_repository)) -> PlaceInDB:
    return await place_repository.add(place)


@router.patch("/update_place/{place_id}", summary="Обновление информации о заведении")
async def update_place(
    place_update: PlaceUpdate,
    place_id: int,
    place_repository: PlaceRepository = Depends(get_place_repository),
) -> PlaceInDB:
    return await place_repository.update(place_id, place_update)


@router.get("/get_place", summary="получение локации по названию")
async def get_place(name: str, place_repository: PlaceRepository = Depends(get_place_repository)) -> PlaceInDB:
    return await place_repository.get_place_by_name(name)
