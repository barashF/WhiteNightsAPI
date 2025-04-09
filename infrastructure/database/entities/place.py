from sqlalchemy import Column, String, Text, Boolean, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from typing import Optional

from .base import Base


class Place(Base):
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    metro: Mapped[str] = mapped_column(String(50))
    avg_rating: Mapped[float] = mapped_column(Float, default=0.0)
    website: Mapped[str] = mapped_column(String(100))

    owner: Mapped["User"] = relationship(
        "User", 
        back_populates="owned_places"
    )



