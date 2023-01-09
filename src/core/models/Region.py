from sqlalchemy import BigInteger

from core.database.database import Base
from sqlmodel import Field, SQLModel, Relationship
from sqlmodel import SQLModel, Field, Column, DateTime


class Region(Base, table=True):
    id: int = Field(nullable=True, sa_column=Column(BigInteger()))
    name: str
    type: str = Field(nullable=True)
