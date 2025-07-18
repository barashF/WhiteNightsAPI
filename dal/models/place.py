from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Place(BaseModel):
    name: str
    description: Optional[str] = None
    address: str
    latitude: float
    longitude: float
    metro: Optional[str] = None
    website: Optional[str] = None
    work_schedule: Optional[str] = None

    @field_validator("latitude")
    def validate_latitude(cls, value):
        if not (-90 <= value <= 90):
            raise ValueError("Широта должна быть между -90 и 90 градусами.")
        return value

    @field_validator("longitude")
    def validate_longitude(cls, value):
        if not (-180 <= value <= 180):
            raise ValueError("Долгота должна быть между -180 и 180 градусами.")
        return value

    @field_validator("website")
    def validate_website(cls, value):
        if value is not None and not value.startswith(("http://", "https://")):
            raise ValueError("Вебсайт должен начинаться с http:// или https://")
        return value

    model_config = ConfigDict(from_attributes=True)


class PlaceInDB(BaseModel):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    metro: Optional[str] = None
    website: Optional[str] = None
    work_schedule: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PlaceUpdate(BaseModel):
    name: Optional[str] = Field(..., max_length=50)
    description: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    metro: Optional[str] = None
    website: Optional[str] = None
    work_schedule: Optional[str] = None
