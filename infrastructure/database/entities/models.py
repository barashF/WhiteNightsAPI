from datetime import datetime
from typing import List

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    avatar: Mapped[str] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    groups: Mapped[List["Group"]] = relationship("Group", secondary="group_members", back_populates="members")


class Place(Base):
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    metro: Mapped[str] = mapped_column(String(50))
    avg_rating: Mapped[float] = mapped_column(Float, default=0.0)
    website: Mapped[str] = mapped_column(String(100))
    work_schedule: Mapped[str] = mapped_column(Text)


class Event(Base):
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    website: Mapped[str] = mapped_column(String(100), nullable=True)
    work_schedule: Mapped[str] = mapped_column(Text)


class Group(Base):
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", onupdate="RESTRICT"))
    owner: Mapped["User"] = relationship("User", lazy="subquery")
    datetime: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    place_id: Mapped[int] = mapped_column(Integer, ForeignKey("places.id", onupdate="RESTRICT"), nullable=True)
    place: Mapped["Place"] = relationship("Place", lazy="subquery")
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey("events.id", onupdate="RESTRICT"), nullable=True)
    event: Mapped["Event"] = relationship("Event", lazy="subquery")
    members: Mapped[List["User"]] = relationship("User", secondary="group_members", back_populates="groups")
    requests: Mapped[List["JoinGroupRequest"]] = relationship("JoinGroupRequest", back_populates="group")


class Group_Member(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=False, nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey("groups.id"), primary_key=True)


class JoinGroupRequest(Base):
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", onupdate="RESTRICT"))
    user: Mapped["User"] = relationship("User", lazy="subquery")
    group_id: Mapped[int] = mapped_column(Integer, ForeignKey("groups.id", onupdate="RESTRICT"))
    group: Mapped["Group"] = relationship("Group", lazy="subquery")
    status: Mapped[str] = mapped_column(String, default="expectation")
