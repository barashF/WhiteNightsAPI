from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from configuration.config import load_config


config = load_config("/app/.env")
# config = load_config("/home/vitaly/Рабочий стол/WhiteNights/.env")
engine = create_async_engine(
    f"postgresql+asyncpg://{config.db.database_user}:{config.db.database_password}@{config.db.database_host}:{config.db.database_port}/{config.db.database_name}",
    future=True,
)
# engine = create_async_engine("sqlite+aiosqlite:///./wn.db", future=True)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncIterator[AsyncSession]:
    async with async_session() as session:
        yield session
