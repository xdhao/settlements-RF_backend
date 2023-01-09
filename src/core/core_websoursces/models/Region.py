from sqlalchemy import BigInteger

from core.core_websoursces.database.database import Base
from sqlmodel import Field, Column


class Region(Base, table=True):
    id: int = Field(nullable=True, sa_column=Column(BigInteger()))
    name: str
    type: str = Field(nullable=True)
