import uuid
from typing import Optional

from core.core_xlsx_parser.database.database import Base
from sqlmodel import Field, Column, Relationship

from core.core_xlsx_parser.models.Country import Country
from core.core_xlsx_parser.models.Population import Population


class FederalDistrict(Base, table=True):
    name: str
    country_guid: uuid.UUID = Field(foreign_key=Country.__pk__, nullable=True)
    population: uuid.UUID = Field(foreign_key=Population.__pk__, nullable=True)

    population_obj: Optional[Population] = Relationship()
    country_obj: Optional[Country] = Relationship()

