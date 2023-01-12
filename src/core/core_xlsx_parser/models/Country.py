import uuid
from typing import Optional

from core.core_xlsx_parser.database.database import Base
from sqlmodel import Field, Column, Relationship

from core.core_xlsx_parser.models.Population import Population


class Country(Base, table=True):
    name: str
    population: uuid.UUID = Field(foreign_key=Population.__pk__, nullable=True)

    population_obj: Optional[Population] = Relationship()

