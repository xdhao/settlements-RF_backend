import uuid
from typing import Optional

from core.core_xlsx_parser.database.database import Base
from sqlmodel import Field, Column, Relationship

from core.core_xlsx_parser.models.FederalDistrict import FederalDistrict
from core.core_xlsx_parser.models.Population import Population


class SomeRegion(Base, table=True):
    name: str
    district_guid: uuid.UUID = Field(foreign_key=FederalDistrict.__pk__, nullable=True)
    population: uuid.UUID = Field(foreign_key=Population.__pk__, nullable=True)

    population_obj: Optional[Population] = Relationship()
    district_obj: Optional[FederalDistrict] = Relationship()


