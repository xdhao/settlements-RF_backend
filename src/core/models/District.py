from core.database.database import Base
from sqlmodel import Field, SQLModel, Relationship
from sqlmodel import SQLModel, Field, Column, DateTime


class District(Base, table=True):
    id: int
    region_id: int = Field(nullable=True)
    name: str
    type: str = Field(nullable=True)
