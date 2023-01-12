import uuid
from typing import Optional

from core.core_xlsx_parser.database.database import Base
from sqlmodel import Field, Column, Relationship

from core.core_xlsx_parser.models.Population import Population
from core.core_xlsx_parser.models.SomeRegion import SomeRegion


class AutonomicDistrict(Base, table=True):
    name: str
    region_guid: uuid.UUID = Field(foreign_key=SomeRegion.__pk__, nullable=True)
    population: uuid.UUID = Field(foreign_key=Population.__pk__, nullable=True)

    population_obj: Optional[Population] = Relationship()
    region_obj: Optional[SomeRegion] = Relationship()
