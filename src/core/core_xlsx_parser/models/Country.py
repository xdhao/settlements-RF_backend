import uuid

from core.core_xlsx_parser.database.database import Base
from sqlmodel import Field, Column

from core.core_xlsx_parser.models.Population import Population


class Country(Base, table=True):
    population: uuid.UUID = Field(foreign_key=Population.__pk__, nullable=True)


