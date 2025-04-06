from sqlalchemy import Column, String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


# class Place(Base):
#     name: Mapped[str] = mapped_column(String())