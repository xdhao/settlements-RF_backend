from core.database.database import Base
from sqlmodel import Field, SQLModel, Relationship
from sqlmodel import SQLModel, Field, Column, DateTime


class Region(Base, table=True):
    id: int
    name: str
    type: str = Field(nullable=True)
