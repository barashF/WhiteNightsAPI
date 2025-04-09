from fastapi import (
    APIRouter, Depends, HTTPException, Query, status
)

from dal.models.user import UserCreate
from infrastructure.repositories.user import UserRepository
from application.di import get_user_repository

router = APIRouter(
    prefix='/user',
    tags=['User']
)


@router.post('/user', summary='тест рег')
async def create_user(user: UserCreate, user_repository: UserRepository = Depends(get_user_repository)):
    return await user_repository.add(user)
