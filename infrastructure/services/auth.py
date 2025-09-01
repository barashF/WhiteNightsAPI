from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from application.di import get_user_repository
from configuration.config import load_config
from dal.interfaces.repositories.user import IUserRepository
from dal.models.user import UserInDB


config = load_config("/app/.env")
# config = load_config("/home/vitaly/Рабочий стол/WhiteNights/.env")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repository: IUserRepository = Depends(get_user_repository),
) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = jwt.decode(token, config.auth.secret_key, algorithms=[config.auth.algorithm])
    email: str = payload.get("email")
    exp: str = payload.get("exp")
    if email is None:
        raise credentials_exception
    if datetime.fromtimestamp(float(exp)) - datetime.now() < timedelta(0):
        raise credentials_exception

    user = await user_repository.get_user_by_email(email, UserInDB)
    if user is None:
        raise credentials_exception
    return user
