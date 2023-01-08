from core.database.database import Base
from sqlmodel import Field, SQLModel, Relationship
from sqlmodel import SQLModel, Field, Column, DateTime


class City(Base, table=True):
    id: int
    region_id: int = Field(nullable=True)
    district_id: int = Field(nullable=True)
    name: str
    people: int = Field(nullable=True)
    area: float = Field(nullable=True)
    head: str = Field(nullable=True)
    type: str = Field(nullable=True)

