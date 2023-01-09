from sqlalchemy import BigInteger

from core.core_xlsx_parser.database.database import Base
from sqlmodel import Field, Column


class People(Base, table=True):
    type: str
    all: int = Field(nullable=True, sa_column=Column(BigInteger()))
    man: int = Field(nullable=True, sa_column=Column(BigInteger()))
    woman: int = Field(nullable=True, sa_column=Column(BigInteger()))
    man_perc: float
    woman_perc: float


