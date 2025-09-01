import re
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from configuration.config import load_config
from dal.interfaces.repositories.user import IUserRepository
from dal.models.token import Token
from dal.models.user import UserAuth, UserCreate, UserInDB


config = load_config("/app/.env")
# config = load_config("/home/vitaly/Рабочий стол/WhiteNights/.env")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/token")


class Validator:
    def validate_email(self, email: str):
        if len(email) > 254:
            raise HTTPException(status_code=400, detail="Email is too long (max 254 characters)")

        pattern = r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$"
        if not re.fullmatch(pattern, email):
            raise HTTPException(status_code=422, detail="Invalid email format")

        parts = email.split("@")
        if len(parts) != 2:
            raise HTTPException(status_code=422, detail="Email must contain exactly one '@' symbol")

        local_part, domain_part = parts

        if len(local_part) > 64:
            raise HTTPException(
                status_code=422,
                detail="Local part (before @) is too long (max 64 characters)",
            )

        if domain_part.startswith(".") or domain_part.endswith(".") or ".." in domain_part:
            raise HTTPException(status_code=422, detail="Invalid domain part")


class AuthFacade:
    def __init__(self, validator: Validator, user_repository: IUserRepository):
        self.validator = validator
        self.user_repository = user_repository

    async def user_registration(self, user_dto: UserCreate) -> UserInDB:
        self.validator.validate_email(user_dto.email)
        return await self.user_repository.add(user_dto)

    async def login_for_access_token(self, email: str, password: str) -> Token:
        user = await self.authenticate_user(email, password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=15)
        access_token = self.create_access_token(data={"email": user.email}, expires_delta=access_token_expires)
        return Token(
            access_token=access_token,
            token_type="bearer",
            access_token_expires=str(access_token_expires),
        )

    def create_access_token(self, data: dict, expires_delta: timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, config.auth.secret_key, config.auth.algorithm)
        return encoded_jwt

    async def authenticate_user(self, email: str, password: str) -> UserCreate:
        user = await self.user_repository.get_user_by_email(email, UserAuth)
        if not user or not self.user_repository.verify_password(password, user.password):
            return False
        return user
