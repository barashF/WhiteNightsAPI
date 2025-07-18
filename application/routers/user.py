from typing import List, Optional

from fastapi import APIRouter, Depends

from application.di import get_registration_facade, get_user_repository
from dal.models.token import Token
from dal.models.user import UserCreate, UserInDB, UserLogin
from infrastructure.repositories.user import UserRepository
from infrastructure.services.auth import get_current_user
from infrastructure.services.registration import AuthFacade


router = APIRouter(prefix="/user", tags=["User"])


@router.post("/reg", summary="тест рег")
async def create_user(
    user: UserCreate,
    registration_facade: AuthFacade = Depends(get_registration_facade),
) -> UserInDB:
    return await registration_facade.user_registration(user)


@router.post("/token")
async def get_token(user: UserLogin, auth_facade: AuthFacade = Depends(get_registration_facade)) -> Token:
    token = await auth_facade.login_for_access_token(user.email, user.password)
    return token


@router.get("/get_all", summary="получить всех")
async def get_all(
    user_repository: UserRepository = Depends(get_user_repository),
) -> List[UserInDB]:
    return await user_repository.get_all_users()


@router.get("/test_token")
async def test(current_user=Depends(get_current_user)):
    return current_user


@router.get("/get_user/{user_id}", summary="юзер по id")
async def get_user(user_id: int, user_repository: UserRepository = Depends(get_user_repository)) -> Optional[UserInDB]:
    return await user_repository.get(user_id)
