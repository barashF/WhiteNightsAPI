from configuration.config import load_config

from contextlib import asynccontextmanager, AbstractContextManager
from typing import AsyncIterator
from logging import Logger

from sqlalchemy import orm
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from infrastructure.database.entities.base import Base

config = load_config('/home/vitaly/Рабочий стол/WhiteNights/.env_test')

engine = create_async_engine('sqlite+aiosqlite:///./wn.db', future=True)
async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        yield session
