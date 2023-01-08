from datetime import datetime

from core.database.database import Base
from sqlmodel import Field, SQLModel, Relationship
from sqlmodel import SQLModel, Field, Column, DateTime


class LastAppealDate(Base, table=True):
    date: datetime = Field(sa_column=Column(DateTime(timezone=True)))


