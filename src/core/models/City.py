from sqlalchemy import BigInteger

from core.database.database import Base
from sqlmodel import Field, SQLModel, Relationship
from sqlmodel import SQLModel, Field, Column, DateTime


class City(Base, table=True):
    id: int = Field(nullable=True, sa_column=Column(BigInteger()))
    region_id: int = Field(nullable=True, sa_column=Column(BigInteger()))
    district_id: int = Field(nullable=True, sa_column=Column(BigInteger()))
    name: str
    people: int = Field(nullable=True)
    area: float = Field(nullable=True)
    head: str = Field(nullable=True)
    type: str = Field(nullable=True)

