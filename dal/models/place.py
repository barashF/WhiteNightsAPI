from pydantic import BaseModel, field_validator, HttpUrl
from typing import Optional

class Place(BaseModel):
    name: str
    description: Optional[str] = None
    address: str
    latitude: float
    longitude: float
    metro: Optional[str] = None
    avg_rating: float = 0.0
    website: Optional[str] = None
    owner_id: int

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
    
    @field_validator("avg_rating")
    def validate_rating(cls, value):
        if not (0 <= value <= 5):
            raise ValueError("Рейтинг должен быть между 0 и 5.")
        return value
    
    @field_validator("website")
    def validate_website(cls, value):
        if value is not None and not value.startswith(('http://', 'https://')):
            raise ValueError("Вебсайт должен начинаться с http:// или https://")
        return value