import uuid
from copy import copy
from datetime import datetime, timezone, timedelta
from typing import Any, Dict

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlmodel import SQLModel, Field, Column, DateTime
from sqlalchemy.orm import sessionmaker, declared_attr, Session

from core.scripts.case import snake_case

SQLALCHEMY_DATABASE_URL_ASYNC = "postgresql+asyncpg://postgres:1234@127.0.0.1:5432/settlements_xlsx_db"
SQLALCHEMY_DATABASE_URL_SYNC = "postgresql://postgres:1234@127.0.0.1:5432/settlements_xlsx_db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL_ASYNC, echo=True, future=True)
engine_sync = create_engine(SQLALCHEMY_DATABASE_URL_SYNC, echo=True)


class IBase(SQLModel):
    @declared_attr
    def __tablename__(cls) -> str:
        """Формирование имени таблицы."""
        # Как есть
        # return cls.__name__

        # Shake case
        return snake_case(cls.__name__)


class Base(IBase):
    """Базовая модель для БД."""
    # __abstract__ = True

    guid: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )

    @declared_attr
    def __pk__(cls) -> str:
        """Первичный ключ таблицы."""
        return f'{cls.__tablename__}.{cls.guid.__dict__["key"]}'


async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

sync_session = sessionmaker(bind=engine_sync)


async def get_session() -> AsyncSession:
    """Получение сессии."""
    async with async_session() as session:
        yield session


def get_session_sync() -> Session:
    with sync_session() as session:
        return session
