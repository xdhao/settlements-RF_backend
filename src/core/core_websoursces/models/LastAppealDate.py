from datetime import datetime

from core.core_websoursces.database.database import Base
from sqlmodel import Field, Column, DateTime


class LastAppealDate(Base, table=True):
    date: datetime = Field(sa_column=Column(DateTime(timezone=True)))


