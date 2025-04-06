from sqlalchemy import Column, String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base


class User(Base):
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    avatar: Mapped[str]
    email: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    bio: Mapped[str] = mapped_column(Text)
    is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)


