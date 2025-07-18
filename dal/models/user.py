from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str = Field(..., max_length=50)
    last_name: str = Field(..., max_length=50)
    username: str = Field(..., max_length=50)
    email: EmailStr = Field(..., max_length=80)


class UserLogin(BaseModel):
    email: str
    password: str


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=255)


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=50)
    last_name: Optional[str] = Field(None, max_length=50)
    username: Optional[str] = Field(None, max_length=50)
    avatar: Optional[str] = Field(None, max_length=255)
    bio: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8, max_length=255)


class UserInDB(UserBase):
    id: int
    avatar: Optional[str] = None
    bio: Optional[str] = None
    is_email_verified: bool = False
    is_superuser: bool = False
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "first_name": "Иван",
                "last_name": "Иванов",
                "username": "ivanov",
                "email": "user@example.com",
                "avatar": "https://example.com/avatar.jpg",
                "bio": "Люблю бухать",
                "is_email_verified": True,
                "is_superuser": False,
                "created_at": "2023-01-01T00:00:00",
            }
        },
    )


class UserAuth(UserInDB):
    password: str
